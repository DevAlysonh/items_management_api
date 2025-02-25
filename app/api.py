from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from uuid import UUID
from app.schema import Item
from app.magalu_api import recuperar_itens_por_pedido
from app.exception import OrderNotFoundException, InternalServerException

app = FastAPI()

def get_items_from_order(order_code: UUID) -> list[Item]:
    return recuperar_itens_por_pedido(order_code)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.get("/orders/{order_code}/items")
def get_items(items: list[Item] = Depends(get_items_from_order)):
    return items

@app.exception_handler(OrderNotFoundException)
def handle(request: Request, exc: OrderNotFoundException):
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Pedido não encontrado"})
@app.exception_handler(InternalServerException)
def tratar_erro_falha_de_comunicacao(request: Request, exc: InternalServerException):
    return JSONResponse(status_code=HTTPStatus.BAD_GATEWAY, content={"message": "Falha de comunicação com o servidor remoto"})