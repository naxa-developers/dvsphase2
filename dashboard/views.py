from django.shortcuts import render, redirect
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import UserForm, ProgramCreateForm, PartnerCreateForm, SectorCreateForm, SubSectorCreateForm, \
    MarkerCategoryCreateForm, MarkerValueCreateForm, GisLayerCreateForm, ProvinceCreateForm, DistrictCreateForm, \
    PalikaCreateForm, IndicatorCreateForm, ProjectCreateForm, PermissionForm, FiveCreateForm, OutputCreateForm, \
    GroupForm
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
    MarkerValues, Indicator, IndicatorValue, GisLayer, Project, PartnerContact, Output
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
    group = Group.objects.get(user=request.user)

    return HttpResponse(group.name)
    # return HttpResponse(kwargs['group'] + kwargs['partner'])
    # return render(request, 'dashboard.html')
    # return HttpResponse(request.user.has_perm('core.add_program'))


@login_required()
def uploadData(request):
    if "GET" == request.method:
        return render(request, 'shapefile.html')
    else:
        csv = request.FILES["shapefile"]
        df = pd.read_csv(csv)
        upper_range = len(df)

        try:
            # fiveData = [
            #     FiveW(
            #         program_name=Program.objects.get(program_name='Naxa'),
            #         partner_name=Partner.objects.get(partner_name='Naxa')
            #     ) for row in range(0, 2)
            # ]

            # five = FiveW.objects.bulk_create(fiveData)
            # list = []
            for row in range(0, upper_range):

                try:
                    partner = Partner.objects.get(program_name=df['IMPLEMENTING PARNTER 1'][row])

                except:
                    partner = None

                try:
                    program = Program.objects.get(program_name=df['PROGRAMME NAME'][row])

                except:
                    program = None

                try:
                    prov = District.objects.get(program_name=df['DISTRICT'][row])

                except:
                    prov = None

                try:
                    district = District.objects.get(program_name=df['DISTRICT'][row])

                except:
                    district = None

                try:
                    palika = GapaNapa.objects.get(program_name=df['Nagarpalika'][row])

                except:
                    palika = None

                try:
                    consortium_1 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER2'][row])

                except:
                    consortium_1 = None

                try:
                    consortium_2 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    consortium_2 = None

                try:
                    consortium_3 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    consortium_3 = None

                try:
                    implementing_1 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    implementing_1 = None

                try:
                    implementing_2 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    implementing_2 = None

                try:
                    implementing_3 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    implementing_3 = None

                try:
                    implementing_4 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    implementing_4 = None

                try:
                    local_1 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    local_1 = None

                try:
                    local_2 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    local_2 = None

                try:
                    local_3 = Partner.objects.get(program_name=df['IMPLEMENTING PARTNER 3'][row])

                except:
                    local_3 = None

                five = FiveW.objects.create(partner_id=partner, program_id=program, province_id=prov,
                                            district_id=district, municipality_id=palika, ward=df['ward'][row],
                                            consortium_partner_first_id=consortium_1,
                                            consortium_partner_second_id=consortium_2,
                                            consortium_partner_third_id=consortium_3,
                                            implementing_partner_first_id=implementing_1,
                                            implementing_partner_second_id=implementing_2,
                                            implementing_partner_third_id=implementing_3,
                                            implementing_partner_fourth_id=implementing_4,
                                            local_partner_first_id=local_1, local_partner_second_id=local_2,
                                            local_partner_third_id=local_3, status=df['status'][row],
                                            reporting_ministry_line=df['reporting_ministry_line'][row],
                                            budget=df['budget'][row])

            # FiveW.objects.create(fiveData)
            # data_list = [1, 2]
            # a = PartnerContact.objects.get(partner_id=58, name='sumit')
            # prog = Partner.objects.get(id='2')
            # progg = Program.objects.get(id='31')
            # progg.partner.add(prog)

            return HttpResponse(five)
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


@login_required()
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

        return redirect('role-list')


@login_required()
def edit_role(request):
    if "GET" == request.method:
        permissions_e = Permission.objects.filter(group__id=9)
        permissions = Permission.objects.all()
        return render(request, 'edit_role.html', {'permissions': permissions, 'permission_e': permissions_e})

    else:
        role = request.POST['role']
        permission_list = request.POST.getlist('permission')
        group = Group.objects.create(name=role)
        for permissions in permission_list:
            permission_check = Permission.objects.get(id=permissions)
            group.permissions.add(permission_check)

        return redirect('role-list')


@login_required()
def assign_role(request, **kwargs):
    if "GET" == request.method:
        groups = Group.objects.all()
        user = request.user
        user_data = UserProfile.objects.get(user=user)
        return render(request, 'assign_role.html', {'user': user_data, 'groups': groups, 'user_id': kwargs['id']})
    else:
        user_id = request.POST['user']
        group_id = request.POST['group_id']
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        user.groups.add(group)
        return redirect('user-list')


@login_required()
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
        emails = request.POST["email"]
        partnered = request.POST["partner"]
        programed = request.POST["program"]
        projected = request.POST["project"]
        subject = 'Thank you for registering to our site'
        message = render_to_string('mail.html', {'group': group, 'url': url, 'partner': partnered, 'program': programed,
                                                 'project': projected})
        recipient_list = [emails]
        email = EmailMessage(
            subject, message, 'from@example.com', recipient_list
        )
        email.content_subtype = "html"
        mail = email.send()
        if mail == 1:
            msg = emails + " was successfully invited"
            messages.success(request, msg)
            return redirect('user-list')
        else:
            msg = emails + " could not be invited "
            messages.success(request, msg)
            return redirect('user-list')


def signup(request, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            if kwargs['group'] != 0:
                group = Group.objects.get(pk=kwargs['group'])
                user.groups.add(group)

            UserProfile.objects.create(user=user, name=request.POST['name'], email=request.POST['email'],
                                       partner_id=int(request.POST['partner']), program_id=int(request.POST['program']),
                                       project_id=int(request.POST['project']), image=request.FILES['image'])

            return render(request, 'created_user.html', {'user': request.POST['name']})

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


class ProgramList(LoginRequiredMixin, ListView):
    template_name = 'program_list.html'
    model = Program

    def get_context_data(self, **kwargs):
        data = super(ProgramList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        if group.name == 'admin':
            program_list = Program.objects.order_by('id')
        else:
            program_list = Program.objects.filter(id=user_data.program.id)
        data['list'] = program_list
        data['user'] = user_data
        data['active'] = 'program'
        return data


class OutputList(LoginRequiredMixin, ListView):
    template_name = 'output_list.html'
    model = Program

    def get_context_data(self, **kwargs):
        data = super(OutputList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        output_list = Output.objects.all()
        data['list'] = output_list
        data['user'] = user_data
        data['active'] = 'output'
        return data


class PermissionList(LoginRequiredMixin, ListView):
    template_name = 'permission_list.html'
    model = Program

    def get_context_data(self, **kwargs):
        data = super(PermissionList, self).get_context_data(**kwargs)
        permission_list = Permission.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = permission_list
        data['user'] = user_data
        data['active'] = 'permission'
        return data


class RoleList(LoginRequiredMixin, ListView):
    template_name = 'role_list.html'
    model = Group

    def get_context_data(self, **kwargs):
        data = super(RoleList, self).get_context_data(**kwargs)
        role_list = Group.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['list'] = role_list
        data['user'] = user_data
        data['active'] = 'permission'
        return data


class FiveList(LoginRequiredMixin, ListView):
    template_name = 'five_list.html'
    model = FiveW

    def get_context_data(self, **kwargs):
        data = super(FiveList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        if group.name == 'admin':
            five = FiveW.objects.order_by('id')
        else:
            five = FiveW.objects.filter(partner_id=user_data.partner.id)
        data['list'] = five
        data['user'] = user_data
        data['active'] = 'five'
        return data


class UserList(LoginRequiredMixin, ListView):
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


class PartnerList(LoginRequiredMixin, ListView):
    template_name = 'partner_list.html'
    model = Partner

    def get_context_data(self, **kwargs):
        data = super(PartnerList, self).get_context_data(**kwargs)
        contact_list = PartnerContact.objects.all().order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        if group.name == 'admin':
            partner_list = Partner.objects.order_by('id')
        else:
            partner_list = Partner.objects.filter(id=user_data.partner.id)

        data['list'] = partner_list
        data['user'] = user_data
        data['active'] = 'partner'
        return data


class SectorList(LoginRequiredMixin, ListView):
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


class ProjectList(LoginRequiredMixin, ListView):
    template_name = 'project_list.html'
    model = Project

    def get_context_data(self, **kwargs):
        data = super(ProjectList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        if group.name == 'admin':
            project_list = Project.objects.order_by('id')
        else:
            project_list = Project.objects.filter(id=user_data.project.id)

        data['list'] = project_list
        data['user'] = user_data
        data['active'] = 'project'
        return data


class SubSectorList(LoginRequiredMixin, ListView):
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


class MarkerList(LoginRequiredMixin, ListView):
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


class MarkerValueList(LoginRequiredMixin, ListView):
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


class IndicatorList(LoginRequiredMixin, ListView):
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


class IndicatorValueList(LoginRequiredMixin, ListView):
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


class GisLayerList(LoginRequiredMixin, ListView):
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


class ProvinceList(LoginRequiredMixin, ListView):
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


class DistrictList(LoginRequiredMixin, ListView):
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


class PalikaList(LoginRequiredMixin, ListView):
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
        group = Group.objects.get(user=user)
        if group.name == 'admin':
            five = FiveW.objects.order_by('id')
        else:
            five = FiveW.objects.select_related('partner_id').filter(partner_id=user_data.partner.id)
        return render(request, 'dashboard.html', {'user': user_data, 'active': 'dash', 'fives': five})


class ProgramAdd(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        return render(request, 'program_add.html', {'user': user_data, 'active': 'program'})


class VectorMap(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'vector_map.html')


class ProgramCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class PartnerCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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
        contact_names = self.request.POST.getlist('contact_person_name')
        emails = self.request.POST.getlist('contact_person_email')
        numbers = self.request.POST.getlist('contact_person_ph')
        upper_range = len(contact_names)
        for row in range(0, upper_range):
            PartnerContact.objects.create(partner_id=self.object, name=contact_names[row], email=emails[row],
                                          phone_number=numbers[row])

        message = "New partner " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class RoleCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'create_role.html'
    form_class = GroupForm
    success_message = 'Role successfully added'

    def get_context_data(self, **kwargs):
        data = super(RoleCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'role'
        data['permissions'] = Permission.objects.all()
        return data

    def get_success_url(self):
        return reverse_lazy('role-list')

    # def form_valid(self, form):
    #     self.object = form.save()
    #     message = "Partner " + self.object.name + "  has been edited by " + self.request.user.username
    #     log = Log.objects.create(user=self.request.user, message=message, type="update")
    #     return HttpResponseRedirect(self.get_success_url())


class SectorCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class OutputCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Output
    template_name = 'output_add.html'
    form_class = OutputCreateForm
    success_message = 'Sector successfully Created'

    def get_context_data(self, **kwargs):
        data = super(OutputCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'output'
        return data

    def get_success_url(self):
        return reverse_lazy('output-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New ouput " + self.object.indicator + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class FiveCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = FiveW
    template_name = 'five_add.html'
    form_class = FiveCreateForm
    success_message = 'Five W successfully Created'

    def get_context_data(self, **kwargs):
        data = super(FiveCreate, self).get_context_data(**kwargs)
        user = self.request.user
        partner = Partner.objects.all().order_by('id')
        program = Program.objects.all().order_by('id')
        project = Project.objects.all().order_by('id')
        province = Province.objects.all().order_by('id')
        district = District.objects.all().order_by('id')
        municipality = GapaNapa.objects.all().order_by('id')
        contact = PartnerContact.objects.all().order_by('id')
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['partners'] = partner
        data['programs'] = program
        data['projects'] = project
        data['provinces'] = province
        data['districts'] = district
        data['municipalities'] = municipality
        data['contacts'] = contact
        return data

    def get_success_url(self):
        return reverse_lazy('five-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Five W " + str(self.object.partner_id) + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class ProjectCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project_add.html'
    form_class = ProjectCreateForm
    success_message = 'Project successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ProjectCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['programs'] = Program.objects.order_by('id')
        data['user'] = user_data
        data['active'] = 'project'
        return data

    def get_success_url(self):
        return reverse_lazy('project-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New project " + self.object.name + "  has been added by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class PermissionCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Permission
    template_name = 'permission_add.html'
    form_class = PermissionForm
    success_message = 'Permission successfully Created'

    def get_context_data(self, **kwargs):
        data = super(PermissionCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'permission'
        return data

    def get_success_url(self):
        return reverse_lazy('permission-list')

    # def form_valid(self, form):
    #     self.object = form.save()
    #     message = "New project " + self.object.name + "  has been added by " + self.request.user.username
    #     log = Log.objects.create(user=self.request.user, message=message, type="create")
    #     return HttpResponseRedirect(self.get_success_url())


class SubSectorCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class ProvinceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class DistrictCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class PalilkaCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class MarkerValueCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class MarkerCategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class IndicatorCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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


class ProgramUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class PartnerUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class RoleUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'edit_role.html'
    form_class = GroupForm
    success_message = 'Role successfully updated'

    def get_context_data(self, **kwargs):
        data = super(RoleUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'role'
        data['permissions'] = Permission.objects.all()
        return data

    def get_success_url(self):
        return reverse_lazy('role-list')

    # def form_valid(self, form):
    #     self.object = form.save()
    #     message = "Partner " + self.object.name + "  has been edited by " + self.request.user.username
    #     log = Log.objects.create(user=self.request.user, message=message, type="update")
    #     return HttpResponseRedirect(self.get_success_url())


class OutputUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Output
    template_name = 'output_edit.html'
    form_class = OutputCreateForm
    success_message = 'Sector successfully Created'

    def get_context_data(self, **kwargs):
        data = super(OutputUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'output'
        return data

    def get_success_url(self):
        return reverse_lazy('output-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Output " + self.object.indicator + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class FiveUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = FiveW
    template_name = 'five_edit.html'
    form_class = FiveCreateForm
    success_message = 'Five W successfully Created'

    def get_context_data(self, **kwargs):
        data = super(FiveUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        partner = Partner.objects.all().order_by('id')
        program = Program.objects.all().order_by('id')
        province = Province.objects.all().order_by('id')
        project = Project.objects.all().order_by('id')
        district = District.objects.all().order_by('id')
        municipality = GapaNapa.objects.all().order_by('id')
        contact = PartnerContact.objects.all().order_by('id')
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['partners'] = partner
        data['programs'] = program
        data['projects'] = project
        data['provinces'] = province
        data['districts'] = district
        data['municipalities'] = municipality
        data['contacts'] = contact
        return data

    def get_success_url(self):
        return reverse_lazy('five-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "New Five W " + str(self.object.partner_id) + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="create")
        return HttpResponseRedirect(self.get_success_url())


class PermissionUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Permission
    template_name = 'permission_add.html'
    form_class = PermissionForm
    success_message = 'Permission successfully edited'

    def get_context_data(self, **kwargs):
        data = super(PermissionUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'permission'
        return data

    def get_success_url(self):
        return reverse_lazy('permission-list')


class SectorUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class ProjectUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = ProjectCreateForm
    success_message = 'Project successfully Created'

    def get_context_data(self, **kwargs):
        data = super(ProjectUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['programs'] = Program.objects.order_by('id')
        data['user'] = user_data
        data['active'] = 'project'
        return data

    def get_success_url(self):
        return reverse_lazy('project-list')

    def form_valid(self, form):
        self.object = form.save()
        message = "Project " + self.object.name + "  has been edited by " + self.request.user.username
        log = Log.objects.create(user=self.request.user, message=message, type="update")
        return HttpResponseRedirect(self.get_success_url())


class SubSectorUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class MarkerCategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class MarkerValueUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class ProvinceUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class DistrictUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class PalilkaUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class IndicatorUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class GisLayerUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class ProgramDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class PartnerDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class SectorDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class SubSectorDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class ProjectDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_message = 'Project successfully deleted'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        data = super(ProjectDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data

    # def delete(self, request, *args, **kwargs):
    #     delete_data = Project.objects.filter(id=kwargs['pk']).delete()
    #     message = "Project  has been deleted by " + self.request.user.username
    #     log = Log.objects.create(user=self.request.user, message=message, type="delete")
    #     return redirect('project-list')


class MarkerCategoryDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class MarkerValueDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class PermissionDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Permission
    template_name = 'permission_confirm_delete.html'
    success_message = 'Permission successfully deleted'
    success_url = reverse_lazy('permission-list')

    def get_context_data(self, **kwargs):
        data = super(PermissionDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class RoleDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'role_confirm_delete.html'
    success_message = 'Permission successfully deleted'
    success_url = reverse_lazy('role-list')

    def get_context_data(self, **kwargs):
        data = super(RoleDelete, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data


class ProvinceDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class DistrictDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class PalikaDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


class IndicatorDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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
