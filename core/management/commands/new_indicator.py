from django.core.management.base import BaseCommand
import os
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from core.models import Indicator
import math


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
        df = df1.fillna('')
        # print(df['Level'][0])
        # print(len(df))
        upper_range = len(df)
        correct_data = []
        for row in range(0, upper_range):
            if df['Indicator '][row] == '':
                pass
            else:
                try:
                    try:
                        test = Indicator.objects.get(indicator=(df['Indicator '][row]).strip())
                        test.full_title = df['Title '][row]
                        test.abstract = df['Abstract'][row]
                        test.category = (df['Category '][row]).strip()
                        test.source = df['Source '][row]
                        test.url = df['URL'][row]
                        test.federal_level = 'all'
                        test.save()
                        self.stdout.write('Successfully Updated' + str(test.full_title) + 'data')
                    except ObjectDoesNotExist:
                        correct_data.append(Indicator(
                            indicator=(df['Indicator '][row]).strip(),
                            full_title=df['Title '][row],
                            abstract=df['Abstract'][row],
                            category=(df['Category '][row]).strip(),
                            source=df['Source '][row],
                            url=df['URL'][row],
                            federal_level='all'
                        ))
                except Exception as e:
                    print(e)
        indicator_data = Indicator.objects.bulk_create(correct_data)
        if indicator_data:
            self.stdout.write('Successfully loaded Indicator data ..')
