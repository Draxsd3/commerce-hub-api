from app.models.product import Product
from app.services.base_service import BaseService


class ProductService(BaseService):
    model = Product

