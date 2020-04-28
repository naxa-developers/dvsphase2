from django.core.management.base import BaseCommand
from core.models import Province, District, GapaNapa
from federal.models import ProvinceBoundary, DistrictBoundary, GapaNapaBoundary
from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def handle(self, *args, **kwargs):

        province_data = Province.objects.exclude(code=-1).order_by('id')
        try:
            self.stdout.write('Starting province  data ..')
            for i in province_data:
                province_update = ProvinceBoundary.objects.create(name=i.name, code=i.code, geom=i.boundary)

            if province_update:
                self.stdout.write('Successfully province updated data ..')
                district_data = District.objects.exclude(code=-1).order_by('id')
                self.stdout.write('Starting district  data ..')
                for i in district_data:
                    district_update = DistrictBoundary.objects.create(
                        province_id=ProvinceBoundary.objects.get(code=i.province_id.code), name=i.name,
                        code=i.code, n_code=i.n_code, geom=i.boundary)

                if district_update:
                    self.stdout.write('Successfully district updated data ..')
                    mun_data = GapaNapa.objects.exclude(code=-1).order_by('id')
                    self.stdout.write('Starting mun  data ..')
                    for i in mun_data:
                        mun_update = GapaNapaBoundary.objects.create(
                            province_id=ProvinceBoundary.objects.get(code=i.province_id.code),
                            district_id=DistrictBoundary.objects.get(code=i.district_id.code), name=i.name,
                            cbs_code=i.cbs_code, hlcit_code=i.hlcit_code,
                            p_code=i.p_code,
                            code=i.code, geom=i.boundary)
                    if mun_update:
                        self.stdout.write('Successfully mun updated data ..')


        except Exception as e:
            print(e)
