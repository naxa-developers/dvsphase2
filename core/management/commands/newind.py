from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Indicator, IndicatorValue, GapaNapa


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    # def add_arguments(self, parser):
    #     parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        # path = kwargs['path']
        #
        # df = pd.read_csv(path)
        # upper_range = len(df)
        print("Wait Data is being Loaded")

        try:
            person = Indicator.objects.get(indicator='hf_per_person')
            new_per = Indicator.objects.get(indicator='hf_per_1000_person')
            print(person.id)
            print(new_per.id)

            data = IndicatorValue.objects.filter(indicator_id=person.id).order_by('id')
            # print(data)
            for d in data:
                print(d.gapanapa_id.id)
                IndicatorValue.objects.create(
                    indicator_id=Indicator.objects.get(id=(new_per.id)),
                    gapanapa_id=GapaNapa.objects.get(id=d.gapanapa_id.id),
                    value=float((d.value) * 1000),
                )




        except Exception as e:
            print(e)
