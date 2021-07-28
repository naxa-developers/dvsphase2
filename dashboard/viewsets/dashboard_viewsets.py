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
         serializer = PartnerSerializer(data=request.data)

         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProgramViewset(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    # serializer_class = SectorGroupSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]


    def list(self, request, *args, **kwargs):
        self.queryset = Program.objects.all()
        return super().list(request, *args, **kwargs)
