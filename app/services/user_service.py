from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import User
from app.services.base_service import BaseService
from app.utils.exceptions import AppError


class UserService(BaseService):
    model = User

    @classmethod
    def create(cls, payload: dict) -> dict:
        try:
            return super().create(payload)
        except IntegrityError as exc:
            db.session.rollback()
            raise AppError("E-mail já cadastrado.", 409) from exc

    @classmethod
    def update(cls, resource_id: int, payload: dict) -> dict:
        try:
            return super().update(resource_id, payload)
        except IntegrityError as exc:
            db.session.rollback()
            raise AppError("Não foi possível atualizar o usuário.", 409) from exc
