from app.utils.exceptions import AppError


def require_fields(payload: dict, fields: list[str]) -> None:
    missing_fields = [field for field in fields if field not in payload or payload[field] in (None, "")]
    if missing_fields:
        raise AppError(
            f"Campos obrigatórios ausentes: {', '.join(missing_fields)}.",
            400,
        )

