from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

from config import HOST, PORT, PASSWORD

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/products-list')
def all_product():
    # return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/create-product')
def create(product: Product):
    return product.save()


@app.get('/product/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/product/{pk}')
def delete(pk: str):
    return Product.delete(pk)

