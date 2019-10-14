from django.contrib.auth.models import User
from django.forms import ModelForm
from core.models import Program, Partner, Sector


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProgramCreateForm(ModelForm):
    class Meta:
        model = Program
        fields = '__all__'


class PartnerCreateForm(ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'


class SectorCreateForm(ModelForm):
    class Meta:
        model = Sector
        fields = '__all__'
