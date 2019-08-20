from django.urls import reverse, resolve


class TestUrls:

    def test_core_partner_url(self):
        path = reverse('partner')
        assert resolve(path).view_name == "partner"

    def test_core_program_url(self):
        path = reverse('program')
        assert resolve(path).view_name == "program"

    def test_core_marker_url(self):
        path = reverse('marker')
        assert resolve(path).view_name == "marker"

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