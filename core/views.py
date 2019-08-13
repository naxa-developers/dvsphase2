from django.shortcuts import render,get_object_or_404
from .models import Organization,Program,MarkerValues
from rest_framework.permissions import AllowAny
from .serializers import OrganizationSerializer,ProgramSerializer,MarkerValuesSerializer
from rest_framework import views
from rest_framework.response import Response
# Create your views here.



class OrganizationView(views.APIView):
    permission_classes=[AllowAny]
    def get(self,request,*args,**kwargs):
        # print(request.user.group)
        queryset=Organization.objects.all()
        serializer=OrganizationSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})


class ProgramView(views.APIView):
    permissions_classes=[AllowAny]
    def get(self,request):
        queryset=Program.objects.all()
        serializer=ProgramSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})


class MarkerView(views.APIView):
    permissions_classes=[AllowAny]
    def get(self,request):
        queryset=MarkerValues.objects.all()
        serializer=MarkerValuesSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})
