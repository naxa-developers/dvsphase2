from .models import FiveW
from django.db.models import Sum


def fivew(supplier, program, component, sector, sub_sector, markers, markers_value, count):
    name_list = ['supplier', 'program', 'component', 'sector', 'sub_sector', 'markers', 'markers_value']
    value_list = [supplier, program, component, sector, sub_sector, markers, markers_value]
    key_list = ['supplier_id__in', 'program_id__in', 'component_id__code__in', 'program_id__sector__id__in',
                'program_id__sub_sector__id__in',
                'program_id__marker_category__id__in', 'program_id__marker_value__id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x and name_list[index] not in count:
            filter_dict[key_list[index]] = x

    dat_values = FiveW.objects.filter(**filter_dict).values('id', 'allocated_budget',
                                                            'component_id',
                                                            'program_id').distinct()

    dat_values = dat_values.exclude(
        municipality_id__code='-1',
        district_id__code='-1',
        province_id__code='-1')
    # print(dat_values.aggregate(Sum('allocated_budget')))
    return dat_values


def fivew_province(province, supplier, program, component, sector, sub_sector, markers, markers_value, count):
    name_list = ['province', 'supplier', 'program', 'component', 'sector', 'sub_sector', 'markers', 'markers_value']
    value_list = [province, supplier, program, component, sector, sub_sector, markers, markers_value]
    key_list = ['province_id__in', 'supplier_id__in', 'program_id__in', 'component_id__code__in',
                'program_id__sector__id__in', 'program_id__sub_sector__id__in',
                'program_id__marker_category__id__in', 'program_id__marker_value__id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x and name_list[index] not in count:
            filter_dict[key_list[index]] = x

    dat_values = FiveW.objects.filter(**filter_dict).values('id', 'allocated_budget',
                                                            'component_id',
                                                            'program_id').distinct()

    dat_values = dat_values.exclude(
        municipality_id__code='-1',
        district_id__code='-1',
        province_id__code='-1')
    return dat_values


def fivew_municipality(municipality, supplier, program, component, sector, sub_sector, markers, markers_value, count):
    name_list = ['municipality', 'supplier', 'program', 'component', 'sector', 'sub_sector', 'markers', 'markers_value']
    value_list = [municipality, supplier, program, component, sector, sub_sector, markers, markers_value]
    key_list = ['municipality_id__in', 'supplier_id__in', 'program_id__in', 'component_id__code__in',
                'program_id__sector__id__in', 'program_id__sub_sector__id__in',
                'program_id__marker_category__id__in', 'program_id__marker_value__id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x and name_list[index] not in count:
            filter_dict[key_list[index]] = x

    dat_values = FiveW.objects.filter(**filter_dict).values('id', 'allocated_budget',
                                                            'component_id',
                                                            'program_id').distinct()
    dat_values = dat_values.exclude(
        municipality_id__code='-1',
        district_id__code='-1',
        province_id__code='-1')
    return dat_values


def fivew_district(district, supplier, program, component, sector, sub_sector, markers, markers_value, count):
    name_list = ['district', 'supplier', 'program', 'component', 'sector', 'sub_sector', 'markers', 'markers_value']
    value_list = [district, supplier, program, component, sector, sub_sector, markers, markers_value]
    key_list = ['district_id__in', 'supplier_id__in', 'program_id__in', 'component_id__code__in',
                'program_id__sector__id__in', 'program_id__sub_sector__id__in',
                'program_id__marker_category__id__in', 'program_id__marker_value__id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x and name_list[index] not in count:
            filter_dict[key_list[index]] = x
    print(filter_dict)
    dat_values = FiveW.objects.filter(**filter_dict).values('id', 'allocated_budget',
                                                            'component_id',
                                                            'program_id').distinct()
    dat_values = dat_values.exclude(
        municipality_id__code='-1',
        district_id__code='-1',
        province_id__code='-1')
    return dat_values
