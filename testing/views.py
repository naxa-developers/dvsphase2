from django.shortcuts import render,get_object_or_404
from .models import Product
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer
from rest_framework import viewsets,views
from rest_framework.response import Response
# Create your views here.


def product_detail(request,pk):
    permission_classes=[]
    product=get_object_or_404(Product,id=pk)
    return render(request,'product.html',{'product':product})


class ProductViewSet(views.APIView):
    permission_classes=[]
    def get(self,request,*args,**kwargs):
        queryset=Product.objects.all()
        serializer=ProductSerializer(queryset,many=True)
        return Response({'heading':'Heading of data','description':'description of data','data':serializer.data})
