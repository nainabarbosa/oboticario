import json
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Compras, Revendedor
from .serializers import RevendedorSerializer, ComprasSerializer, UserSerializer

# tests for views

class BaseViewTest(APITestCase):

    client = APIClient()

    def make_a_request(self, **kwargs):
        return self.client.post(
            reverse(
                "compras"
            ),
            data=json.dumps(kwargs["data"]),
            content_type='application/json'
        )

    def login_a_user(self, username="", password=""):
        url = reverse(
            "login",
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def register_a_user(self, username="", password="", email="", cpf=""):
        return self.client.post(
            reverse("revendedor"),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email,
                    "cpf": cpf
                }
            ),
            content_type='application/json'
        )
    
    def setUp(self):
        self.valid_data = {
            'codigo_compra': 1,
            'data_compra': '2020-04-15',
            'valor': 1.200
        }
        self.invalid_data = {}


class CreateRevendedor(BaseViewTest):

    def test_create_revendedor_with_valid_data(self):
        response = self.register_a_user("testing", "teste123", "testing@mail.com", "12345678911")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_revendedor_with_invalid_data(self):
        response = self.register_a_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ComprasTest(BaseViewTest):

    def test_create_compras_with_valid_data(self):
        response = self.make_a_request(data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_compras_with_invalid_data(self):
        response = self.make_a_request(data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_compras(self):
        response = self.client.get(reverse("compras"))

        # fetch the data from db
        compras_data = Compras.objects.all()
        serialized = ComprasSerializer(compras_data, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CashBackTest(BaseViewTest):

    def test_get_cashback(self):
        response = self.client.get(reverse("acumulado_cashback"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthLoginUserTest(BaseViewTest):

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_with_invalid_credentials(self):
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
