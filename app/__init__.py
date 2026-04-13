import os

from flask import Flask

from app.blueprints.auth.routes import auth_bp
from app.blueprints.orders.routes import orders_bp
from app.blueprints.products.routes import products_bp
from app.blueprints.users.routes import users_bp
from app.config import config_by_name
from app.extensions import db, swagger
from app.utils.error_handlers import register_error_handlers


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    selected_config = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name.get(selected_config, config_by_name["default"]))

    db.init_app(app)
    swagger.init_app(app)

    register_error_handlers(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
