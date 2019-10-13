from django.contrib.auth.models import User
from django.forms import ModelForm
from core.models import Program


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProgramCreateForm(ModelForm):
    class Meta:
        model = Program
        fields = '__all__'
