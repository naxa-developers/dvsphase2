from django.urls import path
# from about_us import viewsets
from .viewsets import AboutUsListApiView, ContactUsListApiView

urlpatterns = [
    path('', AboutUsListApiView.as_view()),
    path('contact_us', ContactUsListApiView.as_view())

]
