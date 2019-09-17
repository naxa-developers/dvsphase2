from django.urls import reverse, resolve


class TestUrls:

    def test_core_partner_url(self):
        path = reverse('partner')
        assert resolve(path).view_name == "partner"

    def test_core_program_url(self):
        path = reverse('program')
        assert resolve(path).view_name == "program"

    def test_core_marker_category_url(self):
        path = reverse('marker-category')
        assert resolve(path).view_name == "marker-category"

    def test_core_marker_value_url(self):
        path = reverse('marker-value')
        assert resolve(path).view_name == "marker-value"

    def test_core_district_url(self):
        path = reverse('district')
        assert resolve(path).view_name == "district"

    def test_core_province_url(self):
        path = reverse('province')
        assert resolve(path).view_name == "province"

    def test_core_gapanapa_url(self):
        path = reverse('gapanapa')
        assert resolve(path).view_name == "gapanapa"

    def test_core_fivew_url(self):
        path = reverse('fivew')
        assert resolve(path).view_name == "fivew"

    def test_core_sector(self):
        path = reverse('sector')
        assert resolve(path).view_name == "sector"

    def test_core_indicator_list(self):
        path = reverse('indicator-list')
        assert resolve(path).view_name == "indicator-list"

    def test_core_indicator_value(self):
        path = reverse('indicator-value')
        assert resolve(path).view_name == "indicator-value"

    def test_core_sub_sector(self):
        path = reverse('sub-sector')
        assert resolve(path).view_name == "sub-sector"