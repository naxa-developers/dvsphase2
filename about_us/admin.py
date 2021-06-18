from django.contrib import admin
from .models import AboutUs, ContactUs
# Register your models here.


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'telephone', 'fax')


admin.site.register(AboutUs)
