from flask_sqlalchemy.model import Model

from app.extensions import db
from app.utils.exceptions import AppError


class BaseService:
    model: type[Model] = None

    @classmethod
    def list_all(cls) -> list[dict]:
        return [item.to_dict() for item in cls.model.query.all()]

    @classmethod
    def get_or_404(cls, resource_id: int):
        instance = cls.model.query.get(resource_id)
        if not instance:
            raise AppError(f"{cls.model.__name__} não encontrado.", 404)
        return instance

    @classmethod
    def create(cls, payload: dict) -> dict:
        instance = cls.model(**payload)
        db.session.add(instance)
        db.session.commit()
        return instance.to_dict()

    @classmethod
    def update(cls, resource_id: int, payload: dict) -> dict:
        instance = cls.get_or_404(resource_id)
        for key, value in payload.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance.to_dict()

    @classmethod
    def delete(cls, resource_id: int) -> None:
        instance = cls.get_or_404(resource_id)
        db.session.delete(instance)
        db.session.commit()

