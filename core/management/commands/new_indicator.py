from django.core.management.base import BaseCommand
import os
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from core.models import Indicator
import math
import json


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        # print(path)
        # print(os.path.exists("/home/sumit/django_projects/dvs/data_csv"))
        # print(os.path.isfile(path))
        df1 = pd.read_csv(path)
        df2 = df1.fillna('')
        df = df2.drop_duplicates(subset=['Indicators'])
        # print(df['Level'][0])
        # print(len(df))
        upper_range = len(df)
        correct_data = []
        for row in range(0, upper_range):
            if df['Indicators'][row] == '':
                pass
            else:
                try:
                    try:
                        test = Indicator.objects.get(indicator=(df['Indicators'][row]).strip())
                        test.full_title = df['Fulltitle'][row]
                        test.abstract = df['Abstract'][row]
                        test.category = (df['Category'][row]).strip()
                        test.source = df['Source'][row]
                        test.url = df['Link'][row]
                        test.federal_level = 'all'
                        test.unit = df['Unit'][row]
                        test.is_dashboard = json.loads(str(df['Show on Dashboard '][row]).lower())
                        test.is_regional_profile = json.loads(str(df['Show on Profile '][row]).lower())
                        test.save()
                        self.stdout.write('Successfully Updated' + str(test.full_title) + 'data')
                    except ObjectDoesNotExist:
                        correct_data.append(Indicator(
                            indicator=(df['Indicators'][row]).strip(),
                            full_title=df['Fulltitle'][row],
                            abstract=df['Abstract'][row],
                            category=(df['Category'][row]).strip(),
                            source=df['Source'][row],
                            url=df['Link'][row],
                            federal_level='all',
                            unit=df['Unit'][row],
                            is_dashboard=json.loads(str(df['Show on Dashboard '][row]).lower()),
                            is_regional_profile=json.loads(str(df['Show on Profile '][row]).lower())
                        ))
                except Exception as e:
                    print(e)
        indicator_data = Indicator.objects.bulk_create(correct_data)
        if indicator_data:
            self.stdout.write('Successfully loaded Indicator data ..')
