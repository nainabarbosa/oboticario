# oboticario
API CashBack O Boticario

## Dependencies

- Python==3.6.9
- Django==3.0.5
- djangorestframework==3.11.0
- djangorestframework-jwt==1.11.0
- PyJWT==1.7.1
- requests==2.23.0

## Running

```
git clone https://github.com/nainabarbosa/oboticario.git
python3 manage.py runserver 0.0.0.0:8000
```

## Usage

```
curl -X GET http://localhost:8000/compras/
curl -X GET http://localhost:8000/acumulado_cashback/
curl -d "username=janaina&password=jana123" http://localhost:8000/login/
curl -d "username=oboticario&password=boti123&email=boti@boticario.com&cpf=123456" http://localhost:8000/revendedor/
curl -d "valor=1000&codigo_compra=1&data_compra=2020-04-15" http://localhost:8000/compras/
```

## Tests

```
python3 manage.py test
```

