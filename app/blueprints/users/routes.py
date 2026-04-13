from flasgger import swag_from
from flask import Blueprint, request

from app.services.user_service import UserService
from app.utils.responses import success_response
from app.utils.validators import require_fields

users_bp = Blueprint("users", __name__)


@users_bp.get("/")
@swag_from({
    "tags": ["Usuários"],
    "summary": "Lista usuários",
    "parameters": [],
    "responses": {
        200: {
            "description": "Lista de usuários",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Usuários listados com sucesso.",
                    "data": [{"id": 1, "name": "Alice"}],
                }
            },
        }
    },
})
def list_users():
    return success_response("Usuários listados com sucesso.", UserService.list_all())


@users_bp.post("/")
@swag_from({
    "tags": ["Usuários"],
    "summary": "Cria um usuário",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "name": "Alice Silva",
                    "email": "alice@example.com",
                    "role": "admin",
                }
            }
        },
    },
    "responses": {
        201: {
            "description": "Usuário criado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Usuário criado com sucesso.",
                    "data": {
                        "id": 1,
                        "name": "Alice Silva",
                        "email": "alice@example.com",
                        "role": "admin",
                    },
                }
            },
        },
        409: {
            "description": "Conflito de e-mail",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "E-mail já cadastrado.",
                    "errors": [],
                }
            },
        },
    },
})
def create_user():
    payload = request.get_json() or {}
    require_fields(payload, ["name", "email", "role"])
    return success_response("Usuário criado com sucesso.", UserService.create(payload), 201)


@users_bp.put("/<int:user_id>")
@swag_from({
    "tags": ["Usuários"],
    "summary": "Atualiza um usuário",
    "parameters": [
        {
            "name": "user_id",
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
                    "name": "Alice Souza",
                    "email": "alice.souza@example.com",
                    "role": "customer",
                }
            }
        },
    },
    "responses": {
        200: {
            "description": "Usuário atualizado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Usuário atualizado com sucesso.",
                    "data": {
                        "id": 1,
                        "name": "Alice Souza",
                        "email": "alice.souza@example.com",
                        "role": "customer",
                    },
                }
            },
        },
        404: {
            "description": "Usuário não encontrado",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "User não encontrado.",
                    "errors": [],
                }
            },
        },
    },
})
def update_user(user_id: int):
    payload = request.get_json() or {}
    return success_response("Usuário atualizado com sucesso.", UserService.update(user_id, payload))


@users_bp.delete("/<int:user_id>")
@swag_from({
    "tags": ["Usuários"],
    "summary": "Remove um usuário",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        200: {
            "description": "Usuário removido",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Usuário removido com sucesso.",
                    "data": None,
                }
            },
        },
        404: {
            "description": "Usuário não encontrado",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "User não encontrado.",
                    "errors": [],
                }
            },
        },
    },
})
def delete_user(user_id: int):
    UserService.delete(user_id)
    return success_response("Usuário removido com sucesso.", None)
