import requests

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from .models import Compras, Revendedor
from .serializers import RevendedorSerializer, ComprasSerializer, UserSerializer, TokenSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RevendedorView(generics.GenericAPIView):
    name='revendedor'
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
    
        """ Esta função irá cadastrar um novo Revendedor.
        O cadastro será feito na tabela de usuários e também na tabela revendedor.
        Irá receber: username, email e cpf
    
        :type dict:
        :param request:
    
        """    
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        cpf = request.data.get("cpf")

        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        novo_usuario = User.objects.create_user(
            username=username, password=password, email=email
        )
        novo_revendedor = Revendedor.objects.create(usuario_id = novo_usuario.id, cpf=cpf)
        return Response(
            data=RevendedorSerializer(novo_revendedor).data,
            status=status.HTTP_201_CREATED
        )


class ComprasView(generics.GenericAPIView):
    name = 'compras'
    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        # Substituir por uma função que busque o revendedor_id usuário logado
        self.revendedor_id = 1
    
    def get_cashback(self, valor):

        """ Esta função irá calcular o percetual e o valor de cashback.

        :type float:
        :param valor:
        """
        if valor <= 1000:
            percent = 10

        elif valor > 1000 or valor <=1500:
            percent = 15

        elif valor > 1500:
            percent = 15

        else:
            percent = 0.00
    
        cashback = round(percent * valor / 100, 2)
        
        return {'percent': percent, 'cashback': cashback}

    def get(self, request):
    
        """ Esta função irá trazer todas as compras do revendedor logado
    
        :type dict:
        :param request:
    
        """    
        compras_data = Compras.objects.filter(revendedor_id=self.revendedor_id)
        serializer = ComprasSerializer(compras_data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
    
        """ Esta função irá criar uma compra para o revendedor logado
        Irá receber como parametro: valor da compra, codigo da compra e data da compra.
    
        :type dict:
        :param request:

        """

        revendedor = Revendedor.objects.filter(pk=self.revendedor_id)
        cpf = revendedor.values()[0]['cpf']

        valor_compra = float(request.data.get('valor'))
        codigo_compra = request.data.get('codigo_compra')
        data_compra = request.data.get('data_compra')
        cashback = self.get_cashback(valor_compra)
        percent_cashback = cashback.get('percent')
        valor_cashback = cashback.get('cashback')
        status_compra = 2

        if cpf != 15350946056:
            status_compra = 1

        compra = Compras.objects.create(
            revendedor_id = self.revendedor_id,
            codigo_compra=codigo_compra,
            valor=valor_compra,
            data_compra=data_compra,
            percent_cashback=percent_cashback,
            valor_cashback=valor_cashback,
            status=status_compra

        )
        return Response(data=compra.id, status=status.HTTP_201_CREATED)


class CashBackView(generics.GenericAPIView):
    name = 'acumulado_cashback'
    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        # Substituir por uma função que busque o revendedor_id usuário logado
        self.revendedor_id = 1
    
    def get(self, request):
    
        """ Essa função irá buscar o acumulado de cashback em uma API externa.
    
        :type dict:
        :param request:
        """

        revendedor = Revendedor.objects.filter(pk=self.revendedor_id)
        cpf = revendedor.values()[0]['cpf']
        result = {}
        if cpf:
            url = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}'.format(cpf)
            token = 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'
            headers = {'Content-Type':'application/json','Authorization':'token ' + token}
            response = requests.get(url, headers=headers)
            if(response.status_code == 200):
                return Response(eval(response.text)['body'])
            else:
                return Response(response.status_code)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):

    name = 'login'
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)