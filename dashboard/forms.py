from django.contrib.auth.models import User, Permission, Group
from django.forms import ModelForm
from core.models import Program, Partner, Sector, SubSector, MarkerCategory, MarkerValues, GisLayer, Province, District, \
    GapaNapa, Indicator, Project, FiveW, Output, BudgetToFirstTier, PartnerContact, Cmp, GisStyle, FeedbackForm, FAQ, \
    TermsAndCondition
from .models import UserProfile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class FeedbackDataForm(ModelForm):
    class Meta:
        model = FeedbackForm
        fields = '__all__'


class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'


class TACForm(ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = '__all__'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'user', 'partner', 'program', 'project']


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'


class ProgramCreateForm(ModelForm):
    class Meta:
        model = Program
        fields = '__all__'


class GroupForm(ModelForm):
    class Meta:
        model = Group
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


class FiveCreateForm(ModelForm):
    class Meta:
        model = FiveW
        fields = '__all__'


class OutputCreateForm(ModelForm):
    class Meta:
        model = Output
        fields = '__all__'


class BudgetCreateForm(ModelForm):
    class Meta:
        model = BudgetToFirstTier
        fields = '__all__'


class PartnerContactForm(ModelForm):
    class Meta:
        model = PartnerContact
        fields = '__all__'


class CmpForm(ModelForm):
    class Meta:
        model = Cmp
        fields = '__all__'


class GisStyleForm(ModelForm):
    class Meta:
        model = GisStyle
        fields = '__all__'
