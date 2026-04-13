from flasgger import swag_from
from flask import Blueprint, request

from app.services.auth_service import AuthService
from app.utils.responses import success_response
from app.utils.validators import require_fields

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/")
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Retorna uma descrição do domínio de autenticação",
    "parameters": [],
    "responses": {
        200: {
            "description": "Informações do domínio",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Domínio de autenticação disponível.",
                    "data": {"resource": "auth"},
                }
            },
        }
    },
})
def auth_overview():
    return success_response("Domínio de autenticação disponível.", {"resource": "auth"})


@auth_bp.post("/")
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Realiza login do usuário",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {"email": "alice@example.com"}
            }
        },
    },
    "responses": {
        200: {
            "description": "Login efetuado com sucesso",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Login realizado com sucesso.",
                    "data": {
                        "access_token": "fake-token-for-user-1",
                        "token_type": "Bearer",
                    },
                }
            },
        },
        401: {
            "description": "Credenciais inválidas",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Credenciais inválidas.",
                    "errors": [],
                }
            },
        },
    },
})
def login():
    payload = request.get_json() or {}
    require_fields(payload, ["email"])
    return success_response("Login realizado com sucesso.", AuthService.login(payload))


@auth_bp.put("/")
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Registra um novo usuário via domínio de autenticação",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "name": "Novo Usuário",
                    "email": "novo@example.com",
                    "role": "customer",
                }
            }
        },
    },
    "responses": {
        200: {
            "description": "Usuário registrado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Usuário registrado com sucesso.",
                    "data": {
                        "id": 10,
                        "name": "Novo Usuário",
                        "email": "novo@example.com",
                        "role": "customer",
                    },
                }
            },
        },
        409: {
            "description": "Conflito de cadastro",
            "examples": {
                "application/json": {
                    "success": False,
                    "message": "Não foi possível registrar o usuário.",
                    "errors": [],
                }
            },
        },
    },
})
def register():
    payload = request.get_json() or {}
    require_fields(payload, ["name", "email", "role"])
    return success_response("Usuário registrado com sucesso.", AuthService.register(payload))


@auth_bp.delete("/")
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Simula logout",
    "responses": {
        200: {
            "description": "Logout efetuado",
            "examples": {
                "application/json": {
                    "success": True,
                    "message": "Logout realizado com sucesso.",
                    "data": None,
                }
            },
        }
    },
})
def logout():
    return success_response("Logout realizado com sucesso.", None)
