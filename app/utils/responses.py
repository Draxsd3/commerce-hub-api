from flask import jsonify


def success_response(message: str, data=None, status_code: int = 200):
    return (
        jsonify(
            {
                "success": True,
                "message": message,
                "data": data,
            }
        ),
        status_code,
    )


def error_response(message: str, status_code: int = 400, errors=None):
    return (
        jsonify(
            {
                "success": False,
                "message": message,
                "errors": errors or [],
            }
        ),
        status_code,
    )

