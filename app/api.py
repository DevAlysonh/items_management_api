from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from uuid import UUID
from app.schema import Item
from app.exception import OrderNotFoundException

app = FastAPI()

def get_items_from_order(order_code: UUID) -> list[Item]:
    pass

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.get("/orders/{order_code}/items")
def get_items(items: list[Item] = Depends(get_items_from_order)):
    return items

@app.exception_handler(OrderNotFoundException)
def handle(request: Request, exc: OrderNotFoundException):
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Pedido não encontrado"})