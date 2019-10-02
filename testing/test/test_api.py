from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase


class TestViews(APITestCase, APIRequestFactory):

    def test_partnernapi(self):
        url = reverse('partner')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_programapi(self):
        url = reverse('program')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_marker_category(self):
        url = reverse('marker-category')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_marker_value(self):
        url = reverse('marker-value')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_districtapi(self):
        url = reverse('district')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_provinceapi(self):
        url = reverse('province')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_gapanapaapi(self):
        url = reverse('gapanapa')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_fivew(self):
        url = reverse('fivew')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_sector(self):
        url = reverse('sector')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    

    def test_indicator_value(self):
        url = reverse('indicator-value')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_sub_sector(self):
        url = reverse('sub-sector')
        response = self.client.get(url, format='json')
        assert response.status_code == 200


