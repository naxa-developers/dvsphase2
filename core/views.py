from django.shortcuts import render,get_object_or_404
from .models import Partner,Program,MarkerValues
from rest_framework.permissions import AllowAny
from .serializers import PartnerSerializer,ProgramSerializer,MarkerValuesSerializer
from rest_framework import views
from rest_framework.response import Response
import django_filters.rest_framework
from django.db.models import Q
# Create your views here.



class PartnerView(views.APIView):
    permission_classes=[AllowAny]
    def get(self,request,*args,**kwargs):
        # print(request.user.group)
        queryset=Partner.objects.all()
        serializer=PartnerSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})


class ProgramView(views.APIView):
    """
    get: list of program
            - parameters: search(from program)
            - description: search should be of type string.
    """
    permissions_classes=[AllowAny]
    def get(self,request):
        search_param = self.request.query_params.get('search', None)
        print(search_param)
        if search_param:
            queryset=Program.objects.filter(Q(program_name__icontains=search_param)| Q(id__icontains=search_param))
        else:
            queryset=Program.objects.all()

        print(queryset)
        serializer=ProgramSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})


class MarkerView(views.APIView):
    permissions_classes=[AllowAny]
    def get(self,request):
        queryset=MarkerValues.objects.all()
        serializer=MarkerValuesSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})
