
from django.conf.urls import url
from .views import LoginView, RevendedorView, ComprasView, LoginView, CashBackView


urlpatterns = [
    url(r'^compras/$', ComprasView.as_view(), name=ComprasView.name),
    url(r'^revendedor/$', RevendedorView.as_view(), name=RevendedorView.name),
    url(r'^acumulado_cashback/$', CashBackView.as_view(), name=CashBackView.name),
    url(r'^login/$', LoginView.as_view(), name=LoginView.name)
]
