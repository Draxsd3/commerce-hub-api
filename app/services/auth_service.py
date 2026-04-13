from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import User
from app.utils.exceptions import AppError


class AuthService:
    @staticmethod
    def login(payload: dict) -> dict:
        email = payload.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            raise AppError("Credenciais inválidas.", 401)

        return {
            "access_token": f"fake-token-for-user-{user.id}",
            "token_type": "Bearer",
            "user": user.to_dict(),
        }

    @staticmethod
    def register(payload: dict) -> dict:
        user = User(name=payload["name"], email=payload["email"], role=payload["role"])
        try:
            db.session.add(user)
            db.session.commit()
            return user.to_dict()
        except IntegrityError as exc:
            db.session.rollback()
            raise AppError("Não foi possível registrar o usuário.", 409) from exc
