from flask import Flask
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.utils.exceptions import AppError
from app.utils.responses import error_response


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        db.session.rollback()
        return error_response(error.message, error.status_code)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(_error: IntegrityError):
        db.session.rollback()
        return error_response("Violação de integridade dos dados.", 409)

    @app.errorhandler(404)
    def handle_not_found(_error):
        return error_response("Recurso não encontrado.", 404)

    @app.errorhandler(500)
    def handle_internal_error(_error):
        db.session.rollback()
        return error_response("Erro interno no servidor.", 500)
