# Generated by Django 3.0.5 on 2020-04-15 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Revendedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=11)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'revendedor',
            },
        ),
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_compra', models.IntegerField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_compra', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(default=1)),
                ('percent_cashback', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_cashback', models.DecimalField(decimal_places=2, max_digits=10)),
                ('revendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashback.Revendedor')),
            ],
            options={
                'db_table': 'compras',
            },
        ),
    ]