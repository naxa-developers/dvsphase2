from core.models import FiveW


def fivew(partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata, group, user_data):
    value_list = [partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata]
    key_list = ['supplier_id__in', 'program_id__in', 'component_id__in', 'province_id__in', 'district_id__in',
                'municipality_id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x:
            filter_dict[key_list[index]] = x

    dat_values = FiveW.objects.filter(**filter_dict).values('id',
                                                            'supplier_id__name',
                                                            'second_tier_partner_name',
                                                            'program_id__name',
                                                            'component_id__name',
                                                            'status',
                                                            'province_id__name',
                                                            'district_id__name',
                                                            'municipality_id__name',
                                                            'allocated_budget').order_by(
        'id')

    if group.name == 'admin':
        return dat_values
    else:
        dat_values = dat_values.filter(supplier_id=user_data.partner.id)
        return dat_values


def export(partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata, group, user_data):
    value_list = [partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata]
    key_list = ['supplier_id__in', 'program_id__in', 'component_id__in', 'province_id__in', 'district_id__in',
                'municipality_id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x:
            filter_dict[key_list[index]] = x
    dat_values = FiveW.objects.filter(**filter_dict).values('id',
                                                            'supplier_id__name',
                                                            'supplier_id__code',
                                                            'second_tier_partner_name',
                                                            'program_id__name',
                                                            'program_id__code',
                                                            'component_id__name',
                                                            'component_id__code',
                                                            'status',
                                                            'province_id__name',
                                                            'province_id__code',
                                                            'district_id__name',
                                                            'district_id__code',
                                                            'municipality_id__name',
                                                            'municipality_id__hlcit_code',
                                                            'allocated_budget',
                                                            'remarks',
                                                            'email',
                                                            'contact_number',
                                                            'contact_name',
                                                            'designation',
                                                            'reporting_line_ministry'
                                                            ).order_by(
        'id')

    if group.name == 'admin':
        return dat_values
    else:
        dat_values = dat_values.filter(supplier_id=user_data.partner.id, component_id=user_data.project.id,
                                       program_id=user_data.program.id)
        return dat_values


def cleardata(partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata, group, user_data):
    value_list = [partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata]
    key_list = ['supplier_id__in', 'program_id__in', 'component_id__in', 'province_id__in', 'district_id__in',
                'municipality_id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x:
            filter_dict[key_list[index]] = x
    dat_values = FiveW.objects.filter(**filter_dict)

    if group.name == 'admin':
        return dat_values
    else:
        dat_values = dat_values.filter(supplier_id=user_data.partner.id, component_id=user_data.project.id,
                                       program_id=user_data.program.id)
        return dat_values
