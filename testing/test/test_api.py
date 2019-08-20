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

    def test_markerapi(self):
        url = reverse('marker')
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

    def test_markerapi(self):
        url = reverse('marker')
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == 200

    def test_districtapi(self):
        url = reverse('district')
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == 200

    def test_provinceapi(self):
        url = reverse('province')
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == 200

    def test_gapanapaapi(self):
        url = reverse('gapanapa')
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == 200
