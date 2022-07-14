import requests
import time
from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request

from config import HOST, PORT, PASSWORD

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# This should be a different database
redis = get_redis_connection(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.get('/order/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/order')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/product/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    # order_completed(order)
    background_tasks.add_task(order_completed, order)
    return order


def order_completed(order: Order):
    time.sleep(2)
    order.status = 'completed'
    order.save()
