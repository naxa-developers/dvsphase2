from django.urls import reverse,resolve


class TestUrls:


    def test_detail_url(self):
        path=reverse('detail',kwargs={'pk':1})
        assert resolve(path).view_name == "detail"

    def test_core_organization_url(self):
        path=reverse('organization')
        assert resolve(path).view_name == "organization"
