from django.contrib.auth.models import User, Group
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from about_us.models import *
from core.serializers import *
from core.models import *
from dashboard.models import UserProfile
from dashboard.tasks import upload_vector_layer


class PartnerViewset(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="Partner - List all partners",
        tags=["Partner"],
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_data = UserProfile.objects.get(user=user)

            group = Group.objects.filter(user=user).values_list("name", flat=True)
            if "admin" in group:
                partner_list = Partner.objects.order_by("id")
            else:
                partner_list = Partner.objects.filter(id=user_data.partner.id)
            serializer = self.get_serializer(partner_list, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @swagger_auto_schema(
        operation_summary="Partner - Retrive partner by id",
        tags=["Partnerss"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partner - Post all partners",
        tags=["Partner"],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance

        partner_serializer = self.serializer_class(instance)
        contact_serializer = PartnerContactSerializer(
            PartnerContact.objects.filter(partner_id=instance), many=True
        )

        headers = self.get_success_headers(serializer.data)
        data = {"partner": partner_serializer.data, "contacts": contact_serializer.data}

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        contact_data = self.request.data.get("contacts", [])
        contacts = []
        for contact in contact_data:
            contacts.append(PartnerContact(partner_id=instance, **contact))
        PartnerContact.objects.bulk_create(contacts)

    @swagger_auto_schema(
        operation_summary="Partner - Partial Update of a partner",
        tags=["Partner"],
    )
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        partner_id = profile.partner_id  # Retrieve the partner ID associated with the logged-in user
        print('partner_id===', partner_id)
        try:
            request_partner_id = int(kwargs.get('pk'))  # Get the partner ID from the URL kwargs
            print('request_partner_id===', request_partner_id)
        except (ValueError, TypeError):
            return Response(
                {"message": "Invalid partner ID provided in the request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request_partner_id == partner_id:
            return super().partial_update(request, *args, **kwargs)  # Call the superclass method for partial update
        else:
            return Response(
                {"message": "Unauthorized to update this partner."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
                
class PartnerContactViewset(viewsets.ModelViewSet):
    queryset = PartnerContact.objects.all()
    serializer_class = PartnerContactSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="Create - PartnerContact",
        tags=["contact"],
    )
    def list(self, request, *args, **kwargs):
        partner_id = request.user.userprofile.partner.id
        if self.queryset == None:
            return Response({"msg": "no data"}, status=status.HTTP_204_NO_CONTENT)
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

    @swagger_auto_schema(
        operation_summary="Retrive - PartnerContact",
        tags=["contact"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - PartnerContact",
        tags=["contact"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ProgramViewset(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Program",
        tags=["program"],
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_data = UserProfile.objects.get(user=user)

            group = Group.objects.filter(user=user).values_list("name", flat=True)
            if "admin" in group:
                program_list = Program.objects.order_by("id")
            else:
                program_list = Program.objects.filter(id=user_data.program.id)
            serializer = self.get_serializer(program_list, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

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
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Project",
        tags=["project"],
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_data = UserProfile.objects.get(user=user)

            group = Group.objects.filter(user=user).values_list("name", flat=True)
            if "admin" in group:
                project_list = Project.objects.order_by("id")
            else:
                project_list = Project.objects.filter(id=user_data.project.id)
            serializer = self.get_serializer(project_list, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

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
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - FiveW",
        tags=["five"],
    )
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_data = UserProfile.objects.get(user=user)
            group = Group.objects.filter(user=user).values_list("name", flat=True)
            if "admin" in group:
                fivew = FiveW.objects.all()
            else:
                fivew = FiveW.objects.filter(
                    supplier_id=user_data.partner.id,
                    program_id=user_data.program.id,
                    component_id=user_data.project.id,
                )

            serializer = self.get_serializer(fivew, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @swagger_auto_schema(
        operation_summary="Create - FiveW",
        tags=["five"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - FiveW",
        tags=["five"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class SectorViewset(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SectorSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

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

    @swagger_auto_schema(
        operation_summary="Update - Sector",
        tags=["sector"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class SubSectorViewset(viewsets.ModelViewSet):
    queryset = SubSector.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubsectorSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

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

    @swagger_auto_schema(
        operation_summary="Update - Sub Sector",
        tags=["sub-sector"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class MarkerCategoryViewset(viewsets.ModelViewSet):
    queryset = MarkerCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MarkerCategorySerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

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

    @swagger_auto_schema(
        operation_summary="Update - MarkerCategory",
        tags=["marker-category"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class MarkerValueViewset(viewsets.ModelViewSet):
    queryset = MarkerValues.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MarkerValuesSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

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

    @swagger_auto_schema(
        operation_summary="Update - MarkerValues",
        tags=["marker-value"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class IndicatorViewset(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = IndicatorSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Indicator",
        tags=["indicator"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Indicator",
        tags=["indicator"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - MarkerValues",
        tags=["indicator"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ProvinceViewset(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProvinceSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post" "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Province",
        tags=["province"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Province",
        tags=["province"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - Province",
        tags=["province"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DistrictSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - District",
        tags=["district"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - District",
        tags=["district"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - District",
        tags=["district"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class PalikaViewset(viewsets.ModelViewSet):
    queryset = GapaNapa.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GaanapaSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Palika",
        tags=["palika"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Palika",
        tags=["palika"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - Palika",
        tags=["palika"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class OutputViewset(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OutputSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Output",
        tags=["output"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Output",
        tags=["output"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - Palika",
        tags=["output"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class GroupManagementViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Group",
        tags=["group"],
    )
    def list(self, request, *args, **kwargs):
        self.serializer_class = GetGroupSerializer
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Group",
        tags=["group"],
    )
    def create(self, request, *args, **kwargs):
        self.serializer_class = GroupSerializer
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update - Group",
        tags=["group"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - User",
        tags=["UserProfile"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - User",
        tags=["UserProfile"],
    )
    def create(self, request, *args, **kwargs):
        try:
            user_serializer = self.get_serializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_instance = user_serializer.save()
            group = Group.objects.get(id=request.data.get("group"))
            user_instance.groups.add(group)

            # Create UserProfile associated with the user
            profile_data = {
                "user": user_instance.id,
                "name": request.data.get("name"),
                "email": request.data.get("email"),
                "partner": request.data.get("partner"),
                "program": request.data.get("program"),
                "project": request.data.get("project"),
            }

            profile_serializer = UserProfileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

            response_data = {
                "user": user_serializer.data,
                "profile": profile_serializer.data,
            }

            headers = self.get_success_headers(user_serializer.data)
            return Response(
                response_data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update - User",
        tags=["sector"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CmpViewset(viewsets.ModelViewSet):
    queryset = Cmp.objects.all()
    serializer_class = CmpSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - Cmp",
        tags=["Cmp"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - Cmp",
        tags=["Cmp"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class FAQViewset(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - FAQ",
        tags=["FAQ"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - FAQ",
        tags=["FAQ"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TermsAndConditionViewset(viewsets.ModelViewSet):
    queryset = TermsAndCondition.objects.all()
    serializer_class = TermsAndConditionSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - TermsAndCondition",
        tags=["TermsAndCondition"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - TermsAndCondition",
        tags=["TermsAndCondition"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AboutUsViewset(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - AboutUs",
        tags=["AboutUs"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - AboutUs",
        tags=["AboutUs"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ContactViewset(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        operation_summary="List - ContactUs",
        tags=["ContactUs"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create - ContactUs",
        tags=["ContactUs"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# Vector Viewset


class VectorLayerViewSet(viewsets.ModelViewSet):
    queryset = VectorLayer.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = VectorLayerDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Vector Layer",
        operation_id="Upload Vector Data",
        tags=["vector layer"],
    )
    def create(self, request, **kwargs):
        """
        Upload Vector Data
        Supported Formats: Shapefile(zipped), Geojson, CSV, KML
        """
        serializer = VectorLayerPostSerializer(data=request.data)
        layer_serializer = LayerPostSerializer(data=request.data)
        name_en = request.data.get("name_en", None)
        if name_en is not None:
            if Layer.objects.filter(name_en=name_en).exists():
                return Response(
                    {"stat": "error", "message": "Name already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if layer_serializer.is_valid():
            layer_object = layer_serializer.save(created_by=request.user)
        else:
            return Response(
                {"stat": "error", "message": layer_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            serializer.save(created_by=request.user, layer=layer_object)

            file_upload = request.data.get("file_upload")
            if file_upload:
                file_id = serializer.data.get("id")
                response = upload_vector_layer(file_id)
                return Response(
                    {
                        "stat": "success",
                        "message": "File upload is in progress",
                        "vector_id": file_id,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"stat": "error", "message": "File Missing"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"stat": "error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_summary="Get List of Vector Layer", tags=["vector layer"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Get Vector Layer ", tags=["vector layer"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Vector Layer by id ", tags=["vector layer"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
