from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APIRequestFactory,APITestCase



class TestViews(APITestCase,APIRequestFactory):

    def test_productapi(self):
        url = reverse('Hydro')
        response = self.client.get(url, format='json')
        assert response.status_code == 200

    def test_organizationapi(self):
        url = reverse('organization')
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == 200

    def test_programapi(self):
        url = reverse('program')
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == 200
