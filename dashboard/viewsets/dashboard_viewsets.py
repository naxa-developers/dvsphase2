# from core.models import (
#     ContactPerson,
#     Country,
#     DevelopmentPartnerGroup,
# )
# from api.serializers.core_serializers import (
#     ContactPersonSerializer,
# )
from core.serializers import *
from core.models import Program, Partner
from dashboard.models import UserProfile
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group, Permission
from rest_framework.response import Response
from rest_framework import status

class PartnerViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @swagger_auto_schema(
        operation_summary="Dashboard - List all partners",
        tags=["dashboard"],
    )

    def list(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                user_data = UserProfile.objects.get(user=user)

                group = Group.objects.filter(user=user).values_list("name", flat=True)
                if 'admin' in group:
                    partner_list = Partner.objects.order_by('id')
                else:
                    partner_list = Partner.objects.filter(id=user_data.partner.id)
                serializer = self.get_serializer(partner_list, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


    @swagger_auto_schema(
        operation_summary="Dashboard - Post all partners",
        tags=["dashboard"],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        instance = serializer.instance
        
        partner_serializer = self.serializer_class(instance)
        contact_serializer = PartnerContactSerializer(PartnerContact.objects.filter(partner_id=instance), many=True)

        headers = self.get_success_headers(serializer.data)
        data = {
            'partner': partner_serializer.data,
            'contacts': contact_serializer.data
        }
        
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        contact_data = self.request.data.get('contacts', [])
        contacts = []
        for contact in contact_data:
            contacts.append(PartnerContact(partner_id=instance, **contact))
        PartnerContact.objects.bulk_create(contacts)


    @swagger_auto_schema(
        operation_summary="Dashboard - Update all partners",
        tags=["dashboard"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class PartnerContactViewset(viewsets.ModelViewSet):
    queryset = PartnerContact.objects.all()
    serializer_class = PartnerContactSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]
    

    @swagger_auto_schema(
        operation_summary="Create - PartnerContact",
        tags=["contact"],
    )
    def list(self, request, *args, **kwargs):
        partner_id = request.user.userprofile.partner.id
        print('partner id==========', partner_id)
        if self.queryset == None:
            return Response({'msg':'no data'}, status=status.HTTP_204_NO_CONTENT)
        else:        
            contact_list = PartnerContact.objects.filter(partner_id=partner_id)
            serializer = self.get_serializer(contact_list, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="List - PartnerContact",
        tags=["contact"],
    )    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProgramViewset(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Program",
        tags=["program"],
    )
    def list(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                user_data = UserProfile.objects.get(user=user)

                group = Group.objects.filter(user=user).values_list("name", flat=True)
                if 'admin' in group:
                    program_list = Program.objects.order_by('id')
                else:
                    program_list = Program.objects.filter(id=user_data.program.id)
                serializer = self.get_serializer(program_list, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


    @swagger_auto_schema(
        operation_summary="Create - Program",
        tags=["program"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update - Program",
        tags=["program"],
    )    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Project",
        tags=["project"],
    )
    def list(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                user_data = UserProfile.objects.get(user=user)

                group = Group.objects.filter(user=user).values_list("name", flat=True)
                if 'admin' in group:
                    project_list = Project.objects.order_by('id')
                else:
                    project_list = Project.objects.filter(id=user_data.project.id)
                serializer = self.get_serializer(project_list, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)



    @swagger_auto_schema(
        operation_summary="Create - Project",
        tags=["project"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update - Project",
        tags=["project"],
    )    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)



class FiveWViewset(viewsets.ModelViewSet):
    queryset = FiveW.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FivewSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - FiveW",
        tags=["five"],
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_data = UserProfile.objects.get(user=user)
            group = Group.objects.filter(user=user).values_list("name", flat=True)
            if 'admin' in group:
                fivew = FiveW.objects.all()
            else:
                fivew = FiveW.objects.filter(supplier_id=user_data.partner.id, program_id=user_data.program.id,
                                            component_id=user_data.project.id) 
                          
            serializer = self.get_serializer(fivew, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_summary="Create - FiveW",
        tags=["five"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SectorViewset(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SectorSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Sector",
        tags=["sector"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Sector",
        tags=["sector"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class SubSectorViewset(viewsets.ModelViewSet):
    queryset = SubSector.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubsectorSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Sub Sector",
        tags=["sub-sector"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Sub Sector",
        tags=["sub-sector"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class MarkerCategoryViewset(viewsets.ModelViewSet):
    queryset = MarkerCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MarkerCategorySerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - MarkerCategory",
        tags=["marker-category"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - MarkerCategory",
        tags=["marker-category"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MarkerValueViewset(viewsets.ModelViewSet):
    queryset = MarkerValues.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MarkerValuesSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - MarkerValues",
        tags=["marker-value"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - MarkerValues",
        tags=["marker-value"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class IndicatorViewset(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = IndicatorSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Indicator",
        tags=["Indicator"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Indicator",
        tags=["Indicator"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ProvinceViewset(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProvinceSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Province",
        tags=["Province"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Province",
        tags=["Province"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DistrictSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - District",
        tags=["District"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - District",
        tags=["District"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class PalikaViewset(viewsets.ModelViewSet):
    queryset = GapaNapa.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GaanapaSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Palika",
        tags=["Palika"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Palika",
        tags=["Palika"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class OutputViewset(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OutputSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Output",
        tags=["Output"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Output",
        tags=["Output"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
