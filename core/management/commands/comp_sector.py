from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Project, Sector, SubSector


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        df = pd.read_csv(path)
        upper_range = len(df)

        print("Wait Data is being Loaded")

        try:
            for row in range(0, upper_range):
                print(df['Component Code'][row])
                a1 = Project.objects.get(code=df['Component Code'][row])
                m1 = Sector.objects.get(name=df['Broad Sectors'][row])
                m2 = SubSector.objects.get(sector_id=m1, name=df['Input Sector'][row])
                data = a1.sector.add(m1)
                data = a1.sub_sector.add(m2)

                # print(a1.name)
                # data = True
            if data:
                self.stdout.write('Successfully loaded  data ..')


        except Exception as e:
            print(e)
