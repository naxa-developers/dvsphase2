from rest_framework import viewsets
from covid.models import (
    CovidFivew,
    DryDshosp4hrSums,
    DryDshosp4hrUncoveredAdm1Sums,
    DryDshosp8hrSums,
    DryDshosp8hrUncoveredAdm1Sums,
    DryDshosp12hrSums,
    DryDshosp12hrUncoveredAdm1Sums,
    DryAllCovidsDhfs4hrSums,
    DryAllCovidsDhfs4hrUncoveredAdm1Sums,
    DryAllCovidsDhfs8hrSums,
    DryAllCovidsDhfs8hrUncoveredAdm1Sums,
    DryAllCovidsDhfs12hrSums,
    DryAllCovidsDhfs12hrUncoveredAdm1Sums,
    CovidSpecificProgram,
    CovidSpecificProgramBudget,
)
from covid.serializers import (
    CovidFivewSerializer,
    DryDshosp4hrSumsSerializer,
    DryDshosp4hrUncoveredAdm1SumsSerializer,
    DryDshosp8hrSumsSerializer,
    DryDshosp8hrUncoveredAdm1SumsSerializer,
    DryDshosp12hrSumsSerializer,
    DryDshosp12hrUncoveredAdm1SumsSerializer,
    DryAllCovidsDhfs4hrSumsSerializer,
    DryAllCovidsDhfs4hrUncoveredAdm1SumsSerializer,
    DryAllCovidsDhfs8hrSumsSerializer,
    DryAllCovidsDhfs8hrUncoveredAdm1SumsSerializer,
    DryAllCovidsDhfs12hrSumsSerializer,
    DryAllCovidsDhfs12hrUncoveredAdm1SumsSerializer,
    CovidSpecificSerializer,
    CovidSpecificBudgetSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend


class TtmpViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = CovidFivew.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = CovidFivewSerializer
        return serializer_class


class CovidSpecificBudget(viewsets.ReadOnlyModelViewSet):
    permission_classes = []

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'district_id', 'municipality_id', 'municipality_id']

    def get_queryset(self):
        queryset = CovidSpecificProgramBudget.objects.order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = CovidSpecificBudgetSerializer
        return serializer_class


class CovidSpecific(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = CovidSpecificProgram.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = CovidSpecificSerializer
        return serializer_class


class DryDshosp4hrSumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryDshosp4hrSums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryDshosp4hrSumsSerializer
        return serializer_class


class DryDshosp4hrUncoveredAdm1SumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryDshosp4hrUncoveredAdm1Sums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryDshosp4hrUncoveredAdm1SumsSerializer
        return serializer_class


class DryDshosp8hrSumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryDshosp8hrSums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryDshosp8hrSumsSerializer
        return serializer_class


class DryDshosp8hrUncoveredAdm1SumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryDshosp8hrUncoveredAdm1Sums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryDshosp8hrUncoveredAdm1SumsSerializer
        return serializer_class


class DryDshosp12hrSumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryDshosp12hrSums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryDshosp12hrSumsSerializer
        return serializer_class


class DryDshosp12hrUncoveredAdm1SumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryDshosp12hrUncoveredAdm1Sums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryDshosp12hrUncoveredAdm1SumsSerializer
        return serializer_class


class DryAllCovidsDhfs4hrSumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryAllCovidsDhfs4hrSums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryAllCovidsDhfs4hrSumsSerializer
        return serializer_class


class DryAllCovidsDhfs4hrUncoveredAdm1SumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryAllCovidsDhfs4hrUncoveredAdm1Sums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryAllCovidsDhfs4hrUncoveredAdm1SumsSerializer
        return serializer_class


class DryAllCovidsDhfs8hrSumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryAllCovidsDhfs8hrSums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryAllCovidsDhfs8hrSumsSerializer
        return serializer_class


class DryAllCovidsDhfs8hrUncoveredAdm1SumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryAllCovidsDhfs8hrUncoveredAdm1Sums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryAllCovidsDhfs8hrUncoveredAdm1SumsSerializer
        return serializer_class


class DryAllCovidsDhfs12hrSumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryAllCovidsDhfs12hrSums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryAllCovidsDhfs12hrSumsSerializer
        return serializer_class


class DryAllCovidsDhfs12hrUncoveredAdm1SumsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "district_id", "municipality_id", "municipality_id"]

    def get_queryset(self):
        queryset = DryAllCovidsDhfs12hrUncoveredAdm1Sums.objects.select_related(
            "district_id", "province_id", "municipality_id"
        ).order_by("id")
        return queryset

    def get_serializer_class(self):
        serializer_class = DryAllCovidsDhfs12hrUncoveredAdm1SumsSerializer
        return serializer_class
