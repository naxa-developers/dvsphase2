from .serializers import AboutUsSerializers, ContactUsSerializers
from .models import AboutUs, ContactUs
from rest_framework.generics import ListAPIView


class AboutUsListApiView(ListAPIView):
    model = AboutUs
    serializer_class = AboutUsSerializers
    queryset = AboutUs.objects.all()


class ContactUsListApiView(ListAPIView):
    model = ContactUs
    serializer_class = ContactUsSerializers
    queryset = ContactUs.objects.all()
