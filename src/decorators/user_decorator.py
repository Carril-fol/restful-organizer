from flask_jwt_extended import get_jwt
from functools import wraps

from services.token_service import TokenService

def is_token_blacklisted(fn):
    """
    Decorator that checks if the JWT token is blacklisted before executing the decorated function.

    Atributes:
    ---------
    fn: The function to be decorated.

    Returns:
    -------
    function: The decorated function that first checks the status of the blacklisted token.
    """ 
    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        try:
            service = TokenService()
            token_jti = get_jwt().get("jti")
            if token_jti is None:
                return {"error": "Token does not contain a jti claim"}, 400
            token_jti_is_blacklisted = service.check_token_if_blacklisted(token_jti)
            if token_jti_is_blacklisted:
                return {"error": "Token is already blacklisted"}, 400
            return await fn(*args, **kwargs)
        except Exception as error:
            return {"error": (str(error))}, 400
    return async_wrapper