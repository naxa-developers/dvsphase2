from django.contrib.auth.models import User, Permission
from django.forms import ModelForm
from core.models import Program, Partner, Sector, SubSector, MarkerCategory, MarkerValues, GisLayer, Province, District, \
    GapaNapa, Indicator, Project


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'


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


class SubSectorCreateForm(ModelForm):
    class Meta:
        model = SubSector
        fields = '__all__'


class MarkerCategoryCreateForm(ModelForm):
    class Meta:
        model = MarkerCategory
        fields = '__all__'


class MarkerValueCreateForm(ModelForm):
    class Meta:
        model = MarkerValues
        fields = '__all__'


class GisLayerCreateForm(ModelForm):
    class Meta:
        model = GisLayer
        fields = '__all__'


class ProvinceCreateForm(ModelForm):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictCreateForm(ModelForm):
    class Meta:
        model = District
        fields = '__all__'


class PalikaCreateForm(ModelForm):
    class Meta:
        model = GapaNapa
        fields = '__all__'


class IndicatorCreateForm(ModelForm):
    class Meta:
        model = Indicator
        fields = '__all__'


class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
