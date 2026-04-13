from flasgger import swag_from
from flask import Blueprint, request

from app.services.product_service import ProductService
from app.utils.responses import success_response
from app.utils.validators import require_fields

products_bp = Blueprint("products", __name__)


@products_bp.get("/")
@swag_from({
    "tags": ["Produtos"],
    "summary": "Lista produtos",
    "parameters": [],
    "responses": {
        200: {
            "description": "Lista de produtos",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Produtos listados com sucesso.",
                    "data": [{"id": 1, "name": "Notebook"}],
                }
            },
        }
    },
})
def list_products():
    return success_response("Produtos listados com sucesso.", ProductService.list_all())


@products_bp.post("/")
@swag_from({
    "tags": ["Produtos"],
    "summary": "Cria um produto",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "name": "Notebook Pro",
                    "description": "Notebook para desenvolvimento",
                    "price": 5999.9,
                    "stock": 15,
                }
            }
        },
    },
    "responses": {
        201: {
            "description": "Produto criado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Produto criado com sucesso.",
                    "data": {
                        "id": 1,
                        "name": "Notebook Pro",
                        "description": "Notebook para desenvolvimento",
                        "price": 5999.9,
                        "stock": 15,
                    },
                }
            },
        },
    },
})
def create_product():
    payload = request.get_json() or {}
    require_fields(payload, ["name", "description", "price", "stock"])
    return success_response("Produto criado com sucesso.", ProductService.create(payload), 201)


@products_bp.put("/<int:product_id>")
@swag_from({
    "tags": ["Produtos"],
    "summary": "Atualiza um produto",
    "parameters": [
        {
            "name": "product_id",
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
                    "price": 5499.9,
                    "stock": 12,
                }
            }
        },
    },
    "responses": {
        200: {
            "description": "Produto atualizado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Produto atualizado com sucesso.",
                    "data": {
                        "id": 1,
                        "name": "Notebook Pro",
                        "description": "Notebook para desenvolvimento",
                        "price": 5499.9,
                        "stock": 12,
                    },
                }
            },
        },
        404: {
            "description": "Produto não encontrado",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Product não encontrado.",
                    "errors": [],
                }
            },
        },
    },
})
def update_product(product_id: int):
    payload = request.get_json() or {}
    return success_response("Produto atualizado com sucesso.", ProductService.update(product_id, payload))


@products_bp.delete("/<int:product_id>")
@swag_from({
    "tags": ["Produtos"],
    "summary": "Remove um produto",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        200: {
            "description": "Produto removido",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Produto removido com sucesso.",
                    "data": None,
                }
            },
        },
        404: {
            "description": "Produto não encontrado",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Product não encontrado.",
                    "errors": [],
                }
            },
        },
    },
})
def delete_product(product_id: int):
    ProductService.delete(product_id)
    return success_response("Produto removido com sucesso.", None)
