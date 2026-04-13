from app.extensions import db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.services.base_service import BaseService
from app.utils.exceptions import AppError


class OrderService(BaseService):
    model = Order

    @classmethod
    def create(cls, payload: dict) -> dict:
        cls._validate_relations(payload)
        product = Product.query.get(payload["product_id"])
        product.stock -= payload["quantity"]
        return super().create(payload)

    @classmethod
    def update(cls, resource_id: int, payload: dict) -> dict:
        order = cls.get_or_404(resource_id)
        cls._restore_previous_stock(order)
        cls._validate_relations(payload, partial=True)
        updated_payload = {
            "user_id": payload.get("user_id", order.user_id),
            "product_id": payload.get("product_id", order.product_id),
            "quantity": payload.get("quantity", order.quantity),
            "status": payload.get("status", order.status),
        }
        cls._validate_relations(updated_payload)
        product = Product.query.get(updated_payload["product_id"])
        product.stock -= updated_payload["quantity"]
        return super().update(resource_id, payload)

    @classmethod
    def delete(cls, resource_id: int) -> None:
        order = cls.get_or_404(resource_id)
        cls._restore_previous_stock(order)
        super().delete(resource_id)

    @staticmethod
    def _validate_relations(payload: dict, partial: bool = False) -> None:
        user_id = payload.get("user_id")
        product_id = payload.get("product_id")

        if user_id is not None and not User.query.get(user_id):
            raise AppError("Usuário informado não existe.", 400)

        if product_id is not None:
            product = Product.query.get(product_id)
            if not product:
                raise AppError("Produto informado não existe.", 400)

            quantity = payload.get("quantity", 1 if partial else None)
            if quantity is not None and product.stock < quantity:
                raise AppError("Estoque insuficiente para o pedido.", 400)

    @staticmethod
    def _restore_previous_stock(order: Order) -> None:
        product = Product.query.get(order.product_id)
        if product:
            product.stock += order.quantity
            db.session.flush()
