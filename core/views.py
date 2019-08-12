from django.shortcuts import render,get_object_or_404
from .models import Organization
from rest_framework.permissions import AllowAny
from .serializers import OrganizationSerializer
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
