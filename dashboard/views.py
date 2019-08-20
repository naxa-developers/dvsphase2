from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from core.models import Program, Partner, FiveW




# Create your views here.
def uploadData(request):
    if "GET" == request.method:
        return render(request, 'dashboard.html')
    else:
        csv = request.FILES["csv_file"]
        df = pd.read_csv(csv)
        org_col = df['ORGANIZATION NAME']
        print(org_col[0])
        try:
            fiveData = [
                FiveW(
                    program_name=Program.objects.get(program_name='Naxa'),
                    partner_name=Partner.objects.get(partner_name='Naxa')
                ) for row in range(0, 2)

            ]
            five = FiveW.objects.bulk_create(fiveData)
            return HttpResponse(str('success'))
        except Exception as e:
            return HttpResponse(e)


