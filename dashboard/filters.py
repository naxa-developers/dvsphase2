from core.models import FiveW


def fivew(partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata):
    value_list = [partnerdata, programdata, projectdata, provincedata, districtdata, municipalitydata]
    key_list = ['supplier_id__in', 'program_id__in', 'component_id__in', 'province_id__in', 'district_id__in',
                'municipality_id__in']
    filter_dict = {}
    for index, x in enumerate(value_list):
        if x:
            filter_dict[key_list[index]] = x

        print(filter_dict)
        print('test')
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

    return dat_values
