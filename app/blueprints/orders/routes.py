from flasgger import swag_from
from flask import Blueprint, request

from app.services.order_service import OrderService
from app.utils.responses import success_response
from app.utils.validators import require_fields

orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/")
@swag_from({
    "tags": ["Pedidos"],
    "summary": "Lista pedidos",
    "parameters": [],
    "responses": {
        200: {
            "description": "Lista de pedidos",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Pedidos listados com sucesso.",
                    "data": [{"id": 1, "status": "pending"}],
                }
            },
        }
    },
})
def list_orders():
    return success_response("Pedidos listados com sucesso.", OrderService.list_all())


@orders_bp.post("/")
@swag_from({
    "tags": ["Pedidos"],
    "summary": "Cria um pedido",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "user_id": 1,
                    "product_id": 1,
                    "quantity": 2,
                    "status": "pending",
                }
            }
        },
    },
    "responses": {
        201: {
            "description": "Pedido criado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Pedido criado com sucesso.",
                    "data": {
                        "id": 1,
                        "user_id": 1,
                        "product_id": 1,
                        "quantity": 2,
                        "status": "pending",
                    },
                }
            },
        },
        400: {
            "description": "Dados inválidos",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Estoque insuficiente para o pedido.",
                    "errors": [],
                }
            },
        },
    },
})
def create_order():
    payload = request.get_json() or {}
    require_fields(payload, ["user_id", "product_id", "quantity", "status"])
    return success_response("Pedido criado com sucesso.", OrderService.create(payload), 201)


@orders_bp.put("/<int:order_id>")
@swag_from({
    "tags": ["Pedidos"],
    "summary": "Atualiza um pedido",
    "parameters": [
        {
            "name": "order_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "status": "completed",
                    "quantity": 1,
                }
            }
        },
    },
    "responses": {
        200: {
            "description": "Pedido atualizado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Pedido atualizado com sucesso.",
                    "data": {
                        "id": 1,
                        "user_id": 1,
                        "product_id": 1,
                        "quantity": 1,
                        "status": "completed",
                    },
                }
            },
        },
        404: {
            "description": "Pedido não encontrado",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Order não encontrado.",
                    "errors": [],
                }
            },
        },
    },
})
def update_order(order_id: int):
    payload = request.get_json() or {}
    return success_response("Pedido atualizado com sucesso.", OrderService.update(order_id, payload))


@orders_bp.delete("/<int:order_id>")
@swag_from({
    "tags": ["Pedidos"],
    "summary": "Remove um pedido",
    "parameters": [
        {
            "name": "order_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        200: {
            "description": "Pedido removido",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Pedido removido com sucesso.",
                    "data": None,
                }
            },
        },
        404: {
            "description": "Pedido não encontrado",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Order não encontrado.",
                    "errors": [],
                }
            },
        },
    },
})
def delete_order(order_id: int):
    OrderService.delete(order_id)
    return success_response("Pedido removido com sucesso.", None)
