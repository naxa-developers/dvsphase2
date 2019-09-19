from django.urls import reverse


def test_token(client, django_user_model):
    username = "test"
    password = "sumit1234"
    url = reverse('token')
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get(url)
    assert response.status_code == 200