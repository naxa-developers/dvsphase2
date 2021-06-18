
from .models import AboutUs, ContactUs
from django.forms import ModelForm


class AboutUsForm(ModelForm):
    class Meta:
        model = AboutUs
        fields = '__all__'


class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
