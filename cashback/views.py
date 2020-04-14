from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from .models import Compras, Revendedor
from .serializers import RevendedorSerializer, ComprasSerializer, UserSerializer


class RevendedorView(generics.GenericAPIView):
    name='revendedor'
    """
    POST revendeor
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
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
        cpf = request.data.get("cpf", "")
        status = 1
        novo_revendedor = Revendedor.objects.create(usuario_id = novo_usuario.id, cpf=cpf)
        return Response(
            data=RevendedorSerializer(new_revendedor).data,
            status=status.HTTP_201_CREATED
        )


class ComprasView(generics.GenericAPIView):
    name = 'compras'
    """
    GET compras/
    POST compras/
    """

    def __init__(self):
        self.revendedor_id = 1
    
    def get_cashback(self, valor):

        if valor <= 1.000:
            percent = 10
            cashback = 0.00

        elif valor > 1.000 or valor <=1500:
            percent = 15
            cashback = 0.00

        elif valor > 1.500:
            percent = 15
            cashback = 0.00

        else:
            percent = 0.00
            cashback = 0.00
        
        return {'percent': percent, 'cashback': cashback}

    def get(self, request):
        compras_data = Compras.objects.filter(revendedor_id=self.revendedor_id)
        serializer = ComprasSerializer(compras_data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        valor_compra = request.data.get('valor')
        codigo_compra = request.data.get('codigo_compra')
        data_compra = request.data.get('data_compra')
        cashback = self.get_cashback(valor)
        percent_cashback = cashback.get('percent')
        valor_cashback = cashback.get('cashback')

        compra = Compras.objects.create(
            revendedor_id = self.revendedor_id,
            codigo_compra=codigo_compra,
            valor=valor_compra,
            data_compra=data_compra,
            percent_cashback=percent_cashback,
            valor_cashback=valor_cashback

        )
        return Response(data=compra.id, status=status.HTTP_201_CREATED)



class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    name = 'login'

    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)