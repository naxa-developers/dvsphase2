from django.shortcuts import render, redirect
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import UserForm, ProgramCreateForm, PartnerCreateForm, SectorCreateForm, SubSectorCreateForm, \
    MarkerCategoryCreateForm, MarkerValueCreateForm, GisLayerCreateForm, ProvinceCreateForm, DistrictCreateForm, \
    PalikaCreateForm, IndicatorCreateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, renderer_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from core.models import Province, Program, FiveW, District, GapaNapa, Partner, Sector, SubSector, MarkerCategory, \
    MarkerValues, Indicator, IndicatorValue, GisLayer, Project
from .models import UserProfile, Log
from django.contrib.auth.models import User, Group, Permission
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from zipfile import ZipFile
import os
from django.contrib import messages
from random import randint
from django.contrib.admin.models import LogEntry


# Create your views here.

@login_required()
def login_test(request, **kwargs):
    # user = authenticate(username='sumit', password='sumit1234')

    # return HttpResponse(request.user)
    # return HttpResponse(kwargs['group'] + kwargs['partner'])
    # return render(request, 'dashboard.html')
    return HttpResponse(request.user.has_perm('core.add_program'))


@login_required()
def uploadData(request):
    if "GET" == request.method:
        return render(request, 'dashboard.html')
    else:
        csv = request.FILES["csv_file"]
        df = pd.read_csv(csv)
        upper_range = len(df)
        org_col = df['ORGANIZATION NAME']

        try:
            # fiveData = [
            #     FiveW(
            #         program_name=Program.objects.get(program_name='Naxa'),
            #         partner_name=Partner.objects.get(partner_name='Naxa')
            #     ) for row in range(0, 2)

            # sdaadassda sadsad

            # ]
            # five = FiveW.objects.bulk_create(fiveData)
            # list = []
            # for row in range(0, upper_range):

            # try:
            #     imp_partner_1 = Partner.objects.get(program_name=df['IMPLEMENTING PARNTER 1'][row])
            #
            # except:
            #     imp_partner_1 = None
            #
            #
            # try:
            #     imp_partner_2 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER2'][row])
            #
            # except:
            #     imp_partner_2 = None
            #
            # try:
            #     imp_partner_3 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])
            #
            # except:
            #     imp_partner_3 = None
            #
            # try:
            #     program = Program.objects.get(program_name=df['PROGRAMME NAME'][row])
            #
            # except:
            #     program = None
            #
            # try:
            #     district = District.objects.get(program_name=df['DISTRICT'][row])
            #
            # except:
            #     district = None
            #
            # try:
            #     nagarpalika = GapaNapa.objects.get(program_name=df['Nagarpalika'][row])
            #
            # except:
            #     nagarpalika = None

            # FiveW.objects.create(fiveData)

            return HttpResponse(df['ORGANIZATION NAME'][0])
        except Exception as e:
            return HttpResponse(e)


# def ShapefileUpload(request):
#     if "GET" == request.method:
#
#         return render(request, 'shapefile.html')
#     else:
#         shapefile = request.FILES["shapefile"]
#         layer_name = 'sumit' + str(randint(0, 9999))
#         # return HttpResponse(layer_name)
#         url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/datastores/' + layer_name + '/file.shp'
#         # return HttpResponse(url)
#
#         headers = {
#             'Content-type': 'application/zip',
#         }
#         response = requests.put(url, headers=headers, data=shapefile, auth=('admin', 'geoserver'))
#         # print(response)
#         return HttpResponse(response.status_code)


def ShapefileUpload(request):
    if "GET" == request.method:

        return render(request, 'shapefile.html')
    else:
        # shapefile = request.FILES["shapefile"]
        get_store_name = GisLayer.objects.filter(id=19).values_list('store_name', flat=True)

        url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/datastores/' + get_store_name[
            0] + '?recurse=true'
        headers = {
            'Content-type': '',
        }
        response = requests.delete(url, headers=headers, auth=('admin', 'geoserver'))
        # print(response)
        return HttpResponse(response.status_code)


def create_role(request):
    if "GET" == request.method:
        permissions = Permission.objects.all()
        return render(request, 'create_role.html', {'permissions': permissions})

    else:
        role = request.POST['role']
        permission_list = request.POST.getlist('permission')
        group = Group.objects.create(name=role)
        for permissions in permission_list:
            permission_check = Permission.objects.get(id=permissions)
            group.permissions.add(permission_check)

        return HttpResponse('success')


def Invitation(request):
    if "GET" == request.method:
        group = Group.objects.all()
        partner = Partner.objects.all()
        program = Program.objects.all()
        project = Project.objects.all()
        return render(request, 'invitation_form.html',
                      {'group': group, 'partners': partner, 'programs': program, 'projects': project})
    else:
        url = settings.SITE_URL
        group = request.POST["group"]
        email = request.POST["email"]
        partnered = request.POST["partner"]
        programed = request.POST["program"]
        projected = request.POST["project"]
        email = request.POST["email"]
        subject = 'Thank you for registering to our site'
        message = render_to_string('mail.html', {'group': group, 'url': url, 'partner': partnered, 'program': programed,
                                                 'project': projected})
        recipient_list = [email]
        email = EmailMessage(
            subject, message, 'from@example.com', recipient_list
        )
        email.content_subtype = "html"
        mail = email.send()

        return HttpResponse(mail)


def signup(request, **kwargs):
    if request.method == 'POST':
        # return HttpResponse(request.POST['partner'])
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            if kwargs['group'] != 0:
                group = Group.objects.get(pk=kwargs['group'])
                user.groups.add(group)

            UserProfile.objects.create(user=user, name=request.POST['name'], email=request.POST['email'],
                                       partner_id=int(request.POST['partner']), program_id=int(request.POST['program']),
                                       project_id=int(request.POST['project']), image=request.FILES['image'])
            return HttpResponse('user created')
    else:
        form = UserCreationForm()
        if kwargs['group'] == 0:
            partner = Partner.objects.all()
            program = Program.objects.all()
            project = Project.objects.all()
        else:
            partner = Partner.objects.filter(id=kwargs['partner'])
            program = Program.objects.filter(id=kwargs['program'])
            project = Project.objects.filter(id=kwargs['project'])

        return render(request, 'signup.html',
                      {'form': form, 'partners': partner, 'programs': program, 'projects': project})


def activate_user(request, **kwargs):
    user = User.objects.get(id=kwargs['id'])
    user.is_active = True
    user.save()
    return redirect('user-list')


@authentication_classes([SessionAuthentication, ])
@api_view()
def auth(request):
    user = request.user
    # return HttpResponse(user)

    if user is None:
        return Response({'error': 'Please authorize first'},
                        status=HTTP_400_BAD_REQUEST)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


def check_login(request):
    if "GET" == request.method:
        form = UserForm()
        return render(request, 'sign_in.html', {'form': form})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        users = authenticate(request, username=username, password=password)
        if users is not None:
            login(request, users)
            return HttpResponse(request.user)
        else:
            return HttpResponse("login failed")


def province_list(request):
    template_name = 'province_list.html'
    province = Program.objects.filter(id=5).order_by('id')
    data_list = Program.objects.filter(id=5).values_list('sector', flat=True)
    user = request.user
    # LogEntry.objects.all().delete()

    if (data_list):
        filter_sector = Sector.objects.order_by('id')

    else:
        filter_sector = Sector.objects.exclude(id__in=data_list)

    data = {}
    data['object_list'] = province
    data['log'] = LogEntry.objects.filter(user_id=user).order_by('-id')[:5]
    data['sector'] = Sector.objects.all().prefetch_related('Sector').order_by('id')
    data['filtered'] = filter_sector
    return render(request, template_name, data)


class ProgramList(ListView):
    template_name = 'program_list.html'
    model = Program

    def get_context_data(self, **kwargs):
        data = super(ProgramList, self).get_context_data(**kwargs)
        program_list = Program.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = program_list
        data['user'] = user_data
        data['active'] = 'program'
        return data


class UserList(ListView):
    template_name = 'user_list.html'
    model = Program

    def get_context_data(self, **kwargs):
        data = super(UserList, self).get_context_data(**kwargs)
        user_list = UserProfile.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = user_list
        data['user'] = user_data
        data['active'] = 'user'
        return data


class PartnerList(ListView):
    template_name = 'partner_list.html'
    model = Partner

    def get_context_data(self, **kwargs):
        data = super(PartnerList, self).get_context_data(**kwargs)
        partner_list = Partner.objects.all().order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = partner_list
        data['user'] = user_data
        data['active'] = 'partner'
        return data


class SectorList(ListView):
    template_name = 'sector_list.html'
    model = Sector

    def get_context_data(self, **kwargs):
        data = super(SectorList, self).get_context_data(**kwargs)
        sector_list = Sector.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = sector_list
        data['user'] = user_data
        data['active'] = 'sector'
        return data


class SubSectorList(ListView):
    template_name = 'sub_sector_list.html'
    model = SubSector

    def get_context_data(self, **kwargs):
        data = super(SubSectorList, self).get_context_data(**kwargs)
        sub_sector_list = SubSector.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = sub_sector_list
        data['user'] = user_data
        data['active'] = 'sector'
        return data


class MarkerList(ListView):
    template_name = 'marker_list.html'
    model = MarkerCategory

    def get_context_data(self, **kwargs):
        data = super(MarkerList, self).get_context_data(**kwargs)
        marker_list = MarkerCategory.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = marker_list
        data['user'] = user_data
        data['active'] = 'marker'
        return data


class MarkerValueList(ListView):
    template_name = 'marker_value_list.html'
    model = MarkerValues

    def get_context_data(self, **kwargs):
        data = super(MarkerValueList, self).get_context_data(**kwargs)
        markervalue_list = MarkerValues.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = markervalue_list
        data['user'] = user_data
        data['active'] = 'marker'
        return data


class IndicatorList(ListView):
    template_name = 'indicator_list.html'
    model = Indicator

    def get_context_data(self, **kwargs):
        data = super(IndicatorList, self).get_context_data(**kwargs)
        indicator_list = Indicator.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = indicator_list
        data['user'] = user_data
        data['active'] = 'indicator'
        return data


class IndicatorValueList(ListView):
    template_name = 'indicator_value_list.html'
    model = Indicator

    def get_context_data(self, **kwargs):
        indicator = self.request.GET['id']
        data = super(IndicatorValueList, self).get_context_data(**kwargs)
        indicator_value_list = IndicatorValue.objects.filter(indicator_id=indicator).order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = indicator_value_list
        data['user'] = user_data
        data['active'] = 'indicator'
        return data


class GisLayerList(ListView):
    template_name = 'gis_layer_list.html'
    model = GisLayer

    def get_context_data(self, **kwargs):
        data = super(GisLayerList, self).get_context_data(**kwargs)
        gis_layer_list = GisLayer.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = gis_layer_list
        data['user'] = user_data
        data['active'] = 'gis'
        return data


class ProvinceList(ListView):
    template_name = 'provinces_list.html'
    model = Province

    def get_context_data(self, **kwargs):
        data = super(ProvinceList, self).get_context_data(**kwargs)
        province = Province.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = province
        data['user'] = user_data
        data['active'] = 'location'
        return data


class DistrictList(ListView):
    template_name = 'district_list.html'
    model = District

    def get_context_data(self, **kwargs):
        data = super(DistrictList, self).get_context_data(**kwargs)

        district = District.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = district
        data['user'] = user_data
        data['active'] = 'location'
        return data


class PalikaList(ListView):
    template_name = 'palika_list.html'
    model = GapaNapa

    def get_context_data(self, **kwargs):
        data = super(PalikaList, self).get_context_data(**kwargs)
        palika = GapaNapa.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['list'] = palika
        data['active'] = 'location'
        return data


class Dashboard(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        return render(request, 'dashboard.html', {'user': user_data, 'active': 'dash'})


class ProgramAdd(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        return render(request, 'program_add.html', {'user': user_data, 'active': 'program'})


class ProgramCreate(SuccessMessageMixin, CreateView):
    model = Program
    template_name = 'program_add.html'
    form_class = ProgramCreateForm
    success_message = 'Program successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ProgramCreate, self).get_context_data(**kwargs)
        sectors = Sector.objects.all().prefetch_related('Sector').order_by('id')
        markers = MarkerCategory.objects.all().prefetch_related('MarkerCategory').order_by('id')
        partners = Partner.objects.all().order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['sectors'] = sectors
        data['markers'] = markers
        data['partners'] = partners
        data['active'] = 'program'
        return data

    def get_success_url(self):
        return reverse_lazy('program-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New program " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class PartnerCreate(SuccessMessageMixin, CreateView):
    model = Partner
    template_name = 'partner_add.html'
    form_class = PartnerCreateForm
    success_message = 'Partner successfully Created'

    def get_context_data(self, **kwargs):
        data = super(PartnerCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'partner'
        return data

    def get_success_url(self):
        return reverse_lazy('partner-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New partner " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class SectorCreate(SuccessMessageMixin, CreateView):
    model = Sector
    template_name = 'sector_add.html'
    form_class = SectorCreateForm
    success_message = 'Sector successfully Created'

    def get_context_data(self, **kwargs):
        data = super(SectorCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'sector'
        return data

    def get_success_url(self):
        return reverse_lazy('sector-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New sector " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class SubSectorCreate(SuccessMessageMixin, CreateView):
    model = SubSector
    template_name = 'sub_sector_add.html'
    form_class = SubSectorCreateForm
    success_message = 'Sub Sector successfully Created'

    def get_context_data(self, **kwargs):
        data = super(SubSectorCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['sectors'] = Sector.objects.order_by('id')
        data['active'] = 'sector'
        return data

    def get_success_url(self):
        return reverse_lazy('subsector-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Sub Sector " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class ProvinceCreate(SuccessMessageMixin, CreateView):
    model = Province
    template_name = 'province_add.html'
    form_class = ProvinceCreateForm
    success_message = 'Province successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ProvinceCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'location'
        return data

    def get_success_url(self):
        return reverse_lazy('province-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New province " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class DistrictCreate(SuccessMessageMixin, CreateView):
    model = District
    template_name = 'district_add.html'
    form_class = DistrictCreateForm
    success_message = 'District successfully Created'

    def get_context_data(self, **kwargs):
        data = super(DistrictCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['active'] = 'location'
        return data

    def get_success_url(self):
        return reverse_lazy('district-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New District " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class PalilkaCreate(SuccessMessageMixin, CreateView):
    model = GapaNapa
    template_name = 'palika_add.html'
    form_class = PalikaCreateForm
    success_message = 'Palika successfully Created'

    def get_context_data(self, **kwargs):
        data = super(PalilkaCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['active'] = 'location'
        return data

    def get_success_url(self):
        return reverse_lazy('palika-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Municipality " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class MarkerValueCreate(SuccessMessageMixin, CreateView):
    model = MarkerValues
    template_name = 'marker_value_add.html'
    form_class = MarkerValueCreateForm
    success_message = 'Marker Value successfully Created'

    def get_context_data(self, **kwargs):
        data = super(MarkerValueCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['sectors'] = MarkerCategory.objects.order_by('id')
        data['active'] = 'marker'
        return data

    def get_success_url(self):
        return reverse_lazy('markervalue-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Marker Value " + self.object.value + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class MarkerCategoryCreate(SuccessMessageMixin, CreateView):
    model = MarkerCategory
    template_name = 'marker_cat_add.html'
    form_class = MarkerCategoryCreateForm
    success_message = 'Marker successfully Created'

    def get_context_data(self, **kwargs):
        data = super(MarkerCategoryCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'marker'
        return data

    def get_success_url(self):
        return reverse_lazy('marker-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Marker Category " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class IndicatorCreate(SuccessMessageMixin, CreateView):
    model = Indicator
    template_name = 'indicator_add.html'
    form_class = IndicatorCreateForm
    success_message = 'Indicator successfully Created'

    def get_context_data(self, **kwargs):
        data = super(IndicatorCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'indicator'
        return data

    def get_success_url(self):
        return reverse_lazy('indicator-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Indicator " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class ProgramUpdate(SuccessMessageMixin, UpdateView):
    model = Program
    template_name = 'program_edit.html'
    form_class = ProgramCreateForm
    success_message = 'Program successfully updated'

    def get_context_data(self, **kwargs):
        data = super(ProgramUpdate, self).get_context_data(**kwargs)
        sector_list = Program.objects.filter(id=self.kwargs['pk']).values_list('sector', flat=True)
        marker_list = Program.objects.filter(id=self.kwargs['pk']).values_list('marker_category', flat=True)
        partner_list = Program.objects.filter(id=self.kwargs['pk']).values_list('partner', flat=True)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)

        if (sector_list[0] == None):
            filter_sector = Sector.objects.order_by('id')

        else:
            filter_sector = Sector.objects.exclude(id__in=sector_list)

        if (marker_list[0] == None):
            filter_marker = MarkerCategory.objects.order_by('id')
        else:
            filter_marker = MarkerCategory.objects.exclude(id__in=marker_list)

        if (partner_list[0] == None):
            filter_partners = Partner.objects.order_by('id')
        else:
            filter_partners = Partner.objects.exclude(id__in=partner_list)

        data['user'] = user_data
        data['sectors'] = filter_sector
        data['test'] = sector_list
        data['markers'] = filter_marker
        data['partners'] = filter_partners
        data['active'] = 'program'
        return data

    def get_success_url(self):
        return reverse_lazy('program-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Program " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class PartnerUpdate(SuccessMessageMixin, UpdateView):
    model = Partner
    template_name = 'partner_edit.html'
    form_class = PartnerCreateForm
    success_message = 'Partner successfully updated'

    def get_context_data(self, **kwargs):
        data = super(PartnerUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'partner'
        return data

    def get_success_url(self):
        return reverse_lazy('partner-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Partner " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class SectorUpdate(SuccessMessageMixin, UpdateView):
    model = Sector
    template_name = 'sector_edit.html'
    form_class = SectorCreateForm
    success_message = 'Sector successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(SectorUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'sector'
        return data

    def get_success_url(self):
        return reverse_lazy('sector-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Sector " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class SubSectorUpdate(SuccessMessageMixin, UpdateView):
    model = SubSector
    template_name = 'sub_sector_edit.html'
    form_class = SubSectorCreateForm
    success_message = 'Sub Sector successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(SubSectorUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['sectors'] = Sector.objects.order_by('id')
        data['active'] = 'sector'
        return data

    def get_success_url(self):
        return reverse_lazy('subsector-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Sub sector " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class MarkerCategoryUpdate(SuccessMessageMixin, UpdateView):
    model = MarkerCategory
    template_name = 'marker_cat_edit.html'
    form_class = MarkerCategoryCreateForm
    success_message = 'Marker Category successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(MarkerCategoryUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'marker'
        return data

    def get_success_url(self):
        return reverse_lazy('marker-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Marker Category " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class MarkerValueUpdate(SuccessMessageMixin, UpdateView):
    model = MarkerValues
    template_name = 'marker_value_edit.html'
    form_class = MarkerValueCreateForm
    success_message = 'Marker Value successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(MarkerValueUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['sectors'] = MarkerCategory.objects.order_by('id')
        data['active'] = 'marker'
        return data

    def get_success_url(self):
        return reverse_lazy('markervalue-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Marker Value " + self.object.value + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class ProvinceUpdate(SuccessMessageMixin, UpdateView):
    model = Province
    template_name = 'province_edit.html'
    form_class = ProvinceCreateForm
    success_message = 'Province successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(ProvinceUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'location'
        return data

    def get_success_url(self):
        return reverse_lazy('province-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Province" + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class DistrictUpdate(SuccessMessageMixin, UpdateView):
    model = District
    template_name = 'district_edit.html'
    form_class = DistrictCreateForm
    success_message = 'District successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(DistrictUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['active'] = 'location'
        return data

    def get_success_url(self):
        return reverse_lazy('district-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "District " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class PalilkaUpdate(SuccessMessageMixin, UpdateView):
    model = GapaNapa
    template_name = 'palika_edit.html'
    form_class = PalikaCreateForm
    success_message = 'Palika successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(PalilkaUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['active'] = 'location'
        return data

    def get_success_url(self):
        return reverse_lazy('palika-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Municipality " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class IndicatorUpdate(SuccessMessageMixin, UpdateView):
    model = Indicator
    template_name = 'indicator_edit.html'
    form_class = IndicatorCreateForm
    success_message = 'Indicator successfully Edited'

    def get_context_data(self, **kwargs):
        data = super(IndicatorUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'indicator'
        return data

    def get_success_url(self):
        return reverse_lazy('indicator-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Indicator " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class GisLayerUpdate(SuccessMessageMixin, UpdateView):
    model = GisLayer
    template_name = 'gis_layer_edit.html'
    form_class = GisLayerCreateForm
    success_message = 'Map Layer successfully Edited'

    def get_context_data(self, **kwargs):
        data = super(GisLayerUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'gis'
        return data

    def get_success_url(self):
        return reverse_lazy('gis-layer-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Map Layer " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class ProgramDelete(SuccessMessageMixin, DeleteView):
    model = Program
    template_name = 'program_confirm_delete.html'
    success_message = 'Program successfully deleted'

    # success_url = reverse_lazy('program-list')

    def get_context_data(self, **kwargs):
        data = super(ProgramDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data

    def get_success_url(self):
        return reverse_lazy('program-list')


class PartnerDelete(SuccessMessageMixin, DeleteView):
    model = Partner
    template_name = 'partner_confirm_delete.html'
    success_message = 'Partner successfully deleted'
    success_url = reverse_lazy('partner-list')

    def get_context_data(self, **kwargs):
        data = super(PartnerDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class SectorDelete(SuccessMessageMixin, DeleteView):
    model = Sector
    template_name = 'sector_confirm_delete.html'
    success_message = 'Sector successfully deleted'
    success_url = reverse_lazy('sector-list')

    def get_context_data(self, **kwargs):
        data = super(SectorDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class SubSectorDelete(SuccessMessageMixin, DeleteView):
    model = SubSector
    template_name = 'sub_sector_confirm_delete.html'
    success_message = 'Sub Sector successfully deleted'
    success_url = reverse_lazy('subsector-list')

    def get_context_data(self, **kwargs):
        data = super(SubSectorDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class MarkerCategoryDelete(SuccessMessageMixin, DeleteView):
    model = MarkerCategory
    template_name = 'marker_cat_confirm_delete.html'
    success_message = 'Marker category successfully deleted'
    success_url = reverse_lazy('marker-list')

    def get_context_data(self, **kwargs):
        data = super(MarkerCategoryDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class MarkerValueDelete(SuccessMessageMixin, DeleteView):
    model = MarkerValues
    template_name = 'marker_value_confirm_delete.html'
    success_message = 'Marker category successfully deleted'
    success_url = reverse_lazy('markervalue-list')

    def get_context_data(self, **kwargs):
        data = super(MarkerValueDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class ProvinceDelete(SuccessMessageMixin, DeleteView):
    model = Province
    template_name = 'province_confirm_delete.html'
    success_message = 'Province successfully deleted'
    success_url = reverse_lazy('province-list')

    def get_context_data(self, **kwargs):
        data = super(ProvinceDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class DistrictDelete(SuccessMessageMixin, DeleteView):
    model = District
    template_name = 'district_confirm_delete.html'
    success_message = 'District successfully deleted'
    success_url = reverse_lazy('district-list')

    def get_context_data(self, **kwargs):
        data = super(DistrictDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class PalikaDelete(SuccessMessageMixin, DeleteView):
    model = GapaNapa
    template_name = 'palika_confirm_delete.html'
    success_message = 'Plaika successfully deleted'
    success_url = reverse_lazy('palika-list')

    def get_context_data(self, **kwargs):
        data = super(PalikaDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class IndicatorDelete(SuccessMessageMixin, DeleteView):
    model = Indicator
    template_name = 'indicator_confirm_delete.html'
    success_message = 'Indicator successfully deleted'
    success_url = reverse_lazy('indicator-list')

    def get_context_data(self, **kwargs):
        data = super(IndicatorDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


def gisLayer_create(request):
    template_name = 'gis_add.html'
    form = GisLayerCreateForm(request.POST or None)
    if form.is_valid():

        shapefile = request.FILES["shapefile"]
        named = request.POST["name"]
        store_named = request.POST["filename"]
        store_name = store_named.replace(" ", "_").lower() + str(randint(0, 99999))

        # return HttpResponse(layer_name)

        if request.POST['type'] == 'vector':

            url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/datastores/' + store_name + '/file.shp'
            headers = {
                'Content-type': 'application/zip',
            }
            response = requests.put(url, headers=headers, data=shapefile, auth=('admin', 'geoserver'))

        else:

            url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/coveragestores/' + store_name + '/file.geotiff'
            headers = {
                'Content-type': 'application/zip',
            }
            response = requests.put(url, headers=headers, data=shapefile, auth=('admin', 'geoserver'))
            # return HttpResponse(response)

        if response.status_code == 201:
            zipfile = ZipFile(shapefile)
            names = zipfile.namelist()
            layer_name = os.path.splitext(names[0])[0]
            obj = form.save(commit=False)
            obj.workspace = 'Naxa'
            obj.layer_name = layer_name
            obj.store_name = store_name
            obj.geoserver_url = 'http://139.59.67.104:8080/geoserver/gwc/service/tms/1.0.0/Naxa:' + layer_name + '@EPSG%3A900913@pbf/{z}/{x}/{-y}.pbf'

            obj.save()
            messaged = "Map Layer " + named + "  has been added by " + request.user.username
            log = Log.objects.create(user=request.user, message=messaged, type="create")
            messages.success(request, "Layer successfully uploaded")

        else:
            messages.error(request, "Layer could not be  uploaded !! Please Try again")

        return redirect('gis-layer-list')
    return render(request, template_name, {'form': form})


def gisLayer_replace(request, **kwargs):
    template_name = 'gis_replace.html'
    instance = GisLayer.objects.get(id=kwargs['pk'])
    get_store_name = GisLayer.objects.filter(id=kwargs['pk']).values_list('store_name', flat=True)
    form = GisLayerCreateForm(request.POST or None, instance=instance)
    # return HttpResponse(instance.store_name)

    if form.is_valid():

        shapefile = request.FILES["shapefile"]
        named = request.POST["name"]
        store_named = request.POST["filename"]
        store_names = store_named.replace(" ", "_").lower() + str(randint(0, 99999999))

        # return HttpResponse(instance.layer_name)

        if request.POST['type'] == 'vector':

            store_check_url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/datastores/' + get_store_name[
                0] + '?recurse=true'

            headers = {
                'Content-type': '',
            }
            response = requests.delete(store_check_url, headers=headers, auth=('admin', 'geoserver'))
            # return HttpResponse(response.status_code)

            url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/datastores/' + store_names + '/file.shp'
            headers = {
                'Content-type': 'application/zip',
            }
            response = requests.put(url, headers=headers, data=shapefile, auth=('admin', 'geoserver'))

        else:

            store_check_url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/coveragestores/' + \
                              get_store_name[0] + '?recurse=true'
            headers = {
                'Content-type': '',
            }
            requests.delete(store_check_url, headers=headers, auth=('admin', 'geoserver'))

            url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/coveragestores/' + store_names + '/file.geotiff'
            headers = {
                'Content-type': 'application/zip',
            }
            response = requests.put(url, headers=headers, data=shapefile, auth=('admin', 'geoserver'))
            # return HttpResponse(response)

        if response.status_code == 201:
            zipfile = ZipFile(shapefile)
            names = zipfile.namelist()
            layer_name = os.path.splitext(names[0])[0]
            obj = form.save(commit=False)
            obj.workspace = 'Naxa'
            obj.store_name = store_names
            obj.layer_name = layer_name
            obj.geoserver_url = 'http://139.59.67.104:8080/geoserver/gwc/service/tms/1.0.0/Naxa:' + layer_name + '@EPSG%3A900913@pbf/{z}/{x}/{-y}.pbf'

            obj.save()
            messaged = "Map Layer " + named + "  has been edited by " + request.user.username
            log = Log.objects.create(user=request.user, message=messaged, type="edited")
            messages.success(request, "Layer successfully replaced")

        else:
            messages.error(request, "Layer could not be  replaced !! Please Try again")

        return redirect('gis-layer-list')
    return render(request, template_name, {'form': form})


def gisLayer_delete(request, **kwargs):
    get_store_name = GisLayer.objects.filter(id=kwargs['pk']).values_list('store_name', flat=True)
    type = GisLayer.objects.filter(id=kwargs['pk']).values_list('type', flat=True)

    if type[0] == 'vector':
        store = 'datastores'
    else:
        store = 'coveragestores'

    store_check_url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/' + store + '/' + get_store_name[
        0] + '?recurse=true'

    headers = {
        'Content-type': '',
    }
    response = requests.get(store_check_url, headers=headers, auth=('admin', 'geoserver'))

    if response.status_code == 200:

        delete_url = 'http://139.59.67.104:8080/geoserver/rest/workspaces/Naxa/' + store + '/' + get_store_name[
            0] + '?recurse=true'

        headers = {
            'Content-type': '',
        }
        delete_response = requests.delete(delete_url, headers=headers, auth=('admin', 'geoserver'))

        if delete_response.status_code == 200:
            delete = GisLayer.objects.filter(id=kwargs['pk']).delete()

        else:
            messages.success(request, "Layer could not be deleted")
            return redirect('gis-layer-list')
    else:

        delete = GisLayer.objects.filter(id=kwargs['pk']).delete()

    if delete:
        messages.success(request, "Layer successfully deleted")
        return redirect('gis-layer-list')
    else:
        messages.success(request, "Layer could not be Deleted")
        return redirect('gis-layer-list')
