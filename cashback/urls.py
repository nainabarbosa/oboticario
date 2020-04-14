
from django.urls import path
from .views import LoginView, RevendedorView, ComprasView, LoginView


urlpatterns = [
    path('compras/$', ListTripsView.as_view(), name=ListTripsView.name),
    path('revendedor/$', LoginView.as_view(), name=LoginView.name),
    path('login/$', LoginView.as_view(), name=LoginView.name)
]