from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Revendedor(models.Model):
    usuario = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)

    class Meta:
        db_table = 'revendedor'

class Compras(models.Model):
    revendedor = models.ForeignKey(Revendedor, null=False, blank=False, on_delete=models.CASCADE)
    codigo_compra = models.IntegerField(null=False, blank=False)
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    data_compra = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=1, null=False, blank=False)
    percent_cashback = models.DecimalField(decimal_places=2, max_digits=10)
    valor_cashback = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'compras'
