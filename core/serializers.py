from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User

from about_us.models import AboutUs, ContactUs
from core.models import (
    Partner,
    PartnerContact,
    Program,
    MarkerValues,
    MarkerCategory,
    District,
    Province,
    GapaNapa,
    FiveW,
    Indicator,
    IndicatorValue,
    Sector,
    SubSector,
    TravelTime,
    GisLayer,
    Project,
    Output,
    Notification,
    BudgetToSecondTier,
    Filter,
    NepalSummary,
    FeedbackForm,
    FAQ,
    TermsAndCondition,
    NationalStatistic,
    Manual,
    Cmp,
    VectorLayer,
    Layer,
)
from dashboard.models import UserProfile


class NepalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = NepalSummary
        fields = "__all__"


class NetionalStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalStatistic
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = "__all__"


class PartnerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerContact
        fields = ["partner_id", "name", "email", "phone_number"]


class DashboardPartnerSerializer(serializers.ModelSerializer):
    contacts = PartnerContactSerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = [
            "id",
            "name",
            "description",
            "type_of_institution",
            "address",
            "email",
            "phone_number",
            "image",
            "thumbnail",
            "code",
            "contacts",
        ]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class MarkerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkerCategory
        fields = "__all__"


class LayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = "__all__"
        read_only = ["id"]


class LayerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ["category", "name_en", "name_ne"]


class VectorLayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorLayer
        fields = "__all__"
        read_only = ["id"]


class VectorLayerDetailSerializer(serializers.ModelSerializer):
    name_en = serializers.SerializerMethodField()
    name_ne = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    layer_type = serializers.SerializerMethodField()

    class Meta:
        model = VectorLayer
        fields = "__all__"
        read_only = ["id"]

    def get_name_en(self, obj):
        return obj.layer.name_en if obj.layer else None

    def get_name_ne(self, obj):
        return obj.layer.name_ne if obj.layer else None

    def get_category(self, obj):
        # return obj.layer.category.id if obj.layer else None
        return obj.layer.category.id if obj.layer and obj.layer.category else None

    def get_order(self, obj):
        return obj.layer.order if obj.layer else None

    def get_layer_type(self, obj):
        return obj.layer.layer_type if obj.layer else None


class VectorLayerListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    bbox = serializers.SerializerMethodField()

    class Meta:
        model = VectorLayer
        fields = "__all__"
        read_only = ["id"]


class GisLayerSerializer(serializers.ModelSerializer):
    style = serializers.SerializerMethodField()
    popup_info = serializers.SerializerMethodField()

    class Meta:
        model = GisLayer
        fields = (
            "id",
            "name",
            "layer_name",
            "workspace",
            "geoserver_url",
            "store_name",
            "type",
            "geo_type",
            "identifier_key",
            "filename",
            "description",
            "style",
            "popup_info",
        )

    def get_style(self, instance):
        styl = []
        styles = instance.GisStyle.all()
        for style in styles:
            styl.append(
                {
                    "id": style.id,
                    "circle_color": style.circle_color,
                    "fill_color": style.fill_color,
                    "circle_radius": style.circle_radius,
                    "layer": style.layer.id,
                }
            )
        return styl

    def get_popup_info(self, instance):
        pop = []
        pops = instance.GisPop.all()
        for p in pops:
            pop.append(
                {
                    "id": p.id,
                    "key": p.key,
                    "title": p.title,
                    "type": p.type,
                    "layer": p.layer.id,
                }
            )
        return pop


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class MarkerValuesSerializer(serializers.ModelSerializer):
    marker_category = serializers.SerializerMethodField()

    class Meta:
        model = MarkerValues
        fields = ("id", "value", "marker_category_id", "marker_category")

    def get_marker_category(self, obj):
        return str(obj.marker_category_id.name)


class DashboardProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "cmp",
            "code",
            "status",
            "total_budget",
            "budget_spend",
            "marker_category",
            "marker_value",
            "sector",
            "sub_sector",
            "sector_budget",
            "iati",
            "program_acronym",
            "partner_id",
        ]


class ProgramSerializer(serializers.ModelSerializer):
    marker_value = serializers.SerializerMethodField()
    marker_category = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    sub_sector = serializers.SerializerMethodField()
    component = serializers.SerializerMethodField()
    partner = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'start_date', 'end_date', 'code', 'iati', 'total_budget', 'partner', 'component',
            'marker_category', 'marker_value',
            'sector',
            'sub_sector', 'program_acronym')

    def get_partner(self, obj):
        data = []
        qs = obj.partner_id.all().values('name', 'id')
        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['name']

            })
        return data

    def get_component(self, obj):
        data = []
        qs = obj.ProjectProgram.values('id', 'name', 'code').distinct('code')
        for q in qs:
            data.append({
                'id': q['id'],
                'code': q['code'],
                'name': q['name']

            })

        return data

    def get_marker_category(self, obj):
        data = []
        qs = obj.marker_value.all().values(
            'marker_category_id', 'marker_category_id__name')
        for q in qs:
            data.append({
                'id': q['marker_category_id'],
                'name': q['marker_category_id__name']

            })
        return data

    def get_marker_value(self, obj):
        data = []
        qs = obj.marker_value.all().values('id', 'value', 'marker_category_id__name')
        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['value'],
                # 'cat': q['marker_category_id__name']

            })
        return data

    def get_sector(self, obj):
        data = []
        qs = obj.sector.all().values('id', 'name').distinct('name')

        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['name']

            })

        return data

    def get_sub_sector(self, obj):
        data = []
        qs = obj.sub_sector.values('id', 'name').distinct('name')

        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['name']

            })

        return data

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("id", "name", "code", "bbox")


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter

        fields = (
            "name",
            "options",
        )


class IndicatorSerializer(serializers.ModelSerializer):
    filter = FilterSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        fields = (
            "id",
            "full_title",
            "indicator",
            "abstract",
            "category",
            "source",
            "federal_level",
            "is_covid",
            "is_dashboard",
            "filter",
            "unit",
            "data_type",
            "url",
        )


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = "__all__"


class SubsectorSerializer(serializers.ModelSerializer):
    sector_name = serializers.SerializerMethodField()

    class Meta:
        model = SubSector
        fields = ("id", "sector_id", "sector_name", "name", "code")

    def get_sector_name(self, obj):
        return str(obj.sector_id.name)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"

    def get_sub_sector(self, obj):
        qs = obj.sub_sector.all().order_by("id").values_list("id", flat=True)
        return qs

    def get_sector(self, obj):
        qs = obj.sector.all().order_by("id").values_list("id", flat=True)
        # qs = obj.sub_sector.all().order_by('id').values('sub_sector_name', 'sub_sector_code')
        return qs

    def get_partners(self, obj):
        qs = obj.partner_id.all().order_by("id").values_list("id", flat=True)
        return qs


class ContractSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetToSecondTier
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    province_name = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = (
            "id",
            "province_id",
            "province_name",
            "name",
            "code",
            "n_code",
            "bbox",
        )

    def get_province_name(self, obj):
        return str(obj.province_id.name)


class GaanapaSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()

    class Meta:
        model = GapaNapa
        fields = (
            "id",
            "province_id",
            "district_id",
            "province_name",
            "district_name",
            "hlcit_code",
            "name",
            "gn_type_np",
            "code",
            "population",
            "bbox",
        )

    def get_code(self, obj):
        return str(obj.code)

    def get_district_name(self, obj):
        return obj.district_id.name

    def get_province_name(self, obj):
        return str(obj.province_id.name)


class FivewSerializer(serializers.ModelSerializer):
    # partner_name = serializers.SerializerMethodField()
    # program_name = serializers.SerializerMethodField()
    # province = serializers.SerializerMethodField()
    # district = serializers.SerializerMethodField()
    # gapa_napa = serializers.SerializerMethodField()
    # implenting_partner_first = serializers.SerializerMethodField()
    # implenting_partner_second = serializers.SerializerMethodField()
    # implenting_partner_third = serializers.SerializerMethodField()

    class Meta:
        model = FiveW
        fields = "__all__"

    #     fields = (
    #         'id', 'partner_name', 'program_name', 'province', 'district', 'gapa_napa', 'status', 'start_date',
    #         'end_date',
    #         'reporting_ministry_line', 'implenting_partner_first', 'implenting_partner_second',
    #         'implenting_partner_third')

    # def get_partner_name(self, obj):
    #     return str(obj.partner_name)
    #
    # def get_program_name(self, obj):
    #     return str(obj.program_name)
    #
    # def get_province(self, obj):
    #     return str(obj.province)
    #
    # def get_district(self, obj):
    #     return str(obj.district)
    #
    # def get_gapa_napa(self, obj):
    #     return str(obj.gapa_napa.name)
    #
    # def get_implenting_partner_first(self, obj):
    #     return str(obj.implenting_partner_first)
    #
    # def get_implenting_partner_second(self, obj):
    #     return str(obj.implenting_partner_second)
    #
    # def get_implenting_partner_third(self, obj):
    #     return str(obj.implenting_partner_third)


class IndicatorValueSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    # indicator_name = serializers.SerializerMethodField()

    class Meta:
        model = IndicatorValue
        fields = ("id", "indicator_id", "code", "value", "name")

    def get_code(self, obj):
        try:
            return str(obj.gapanapa_id.code)
        except:
            return None

    def get_name(self, obj):
        try:
            return str(obj.gapanapa_id.name)
        except:
            return None

    # def get_indicator_name(self, obj):
    #     return str(obj.indicator_id.indicator)


class TravelTimeSerializer(serializers.ModelSerializer):
    gapanapa = serializers.SerializerMethodField()
    geography = serializers.SerializerMethodField()

    class Meta:
        model = TravelTime
        fields = (
            "id",
            "gapanapa",
            "facility_type",
            "travel_category_population",
            "tc_pc_pop",
            "season",
            "geography",
            "travel_category",
        )

    def get_gapanapa(self, obj):
        return str(obj.gapanapa)

    def get_geography(self, obj):
        return str(obj.gapanapa.geography)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackForm
        fields = ["name", "email", "attachment", "subject", "your_feedback", "type"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
        )


class GetGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id', 'username', 'email', 'password')
        fields = ("username", "password")
        extra_kwargs = {
            "password": {
                "write_only": True
            },  # Password should only be written, not displayed
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "name",
            "email",
            "partner",
            "program",
            "project",
            "image",
            "thumbnail",
            "user",
        )


class CmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cmp
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
