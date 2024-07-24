from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

from auth.services.user_service import UserService
from auth.services.token_service import TokenService
from auth.decorators.user_decorator import is_token_blacklisted
from auth.exceptions.user_exceptions import UserAlreadyExists, UserNotFoundException, PasswordDontMatch
from auth.exceptions.token_exceptions import TokenAlreadyBlacklisted

user_service = UserService()
token_service = TokenService()

class UserRegisterResource(Resource):
    """
    Example:

    POST: /users/register

    ```
    Application data:
    {
        "first_name": "First name from the user",
        "last_name": "Last name from the user",
        "email": "Email from the user",
        "password": "Password from the user",
        "confirm_password": "Confirmation from the password"
    }

    Successful response (code 201 - CREATED):
    {   
        "msg": "User created",
        "user": {
            "id": "Id from the user",
            "first_name": "First name from the user",
            "last_name": "Last name from the user",
            "email": "Email from the user",
            "password": "Password from the user",
            "confirm_password": "Confirmation from the password"
        },
        "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUedsXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Response with validation errors (code 400 - BAD REQUEST):
    {
        "email": ["This field has to be unique"],
        "password": ["Password must contain at least one number."],
        // Other errors of validation from the schema.
    }
    ```
    """
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400       
        try:
            new_user = user_service.create_user(data)
            user_json = user_service.get_user_by_id(new_user)
            access_token = create_access_token(user_json)
            return {"msg": "User created", "user": user_json, "access_token": access_token}, 201
        except UserAlreadyExists as error:
            return {"error": (str(error))}, 400
        except Exception as error:
            return {"error": (str(error))}, 400


class UserLoginResource(Resource):
    """
    Example:

    POST: /users/login

    ```
    Application data:
    {
        "email": "Email from the user",
        "password": "Password from the user"
    }

    Successful response (code 200 - OK):
    {
        "message": "Login successful"
        "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUed.sXiwp31A4wQ6klpJclPYQyZDsFruLuybCsd..."
        "refresh_token": "8uP9dv0czfTLY8WEma1fZyBYLzUed.sXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Response with errors (code 400 - BAD REQUEST):
    {
        "email": "This field has to be unique.",
        // Other errors of validation from the schema.
    }
    ```
    """
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        try:
            user_exists = user_service.authenticate_user(data)
            refresh_token = create_refresh_token(user_exists)
            access_token = create_access_token(user_exists)
            return {"msg": "Login succefully", "tokens": { "access_token": access_token, "refresh_token": refresh_token}}, 200
        except PasswordDontMatch as error:
            return {"error": (str(error))}, 400
        except UserNotFoundException as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400


class UserDetailsResource(Resource):
    """
    Example:

    GET: /users/<user_id>
    ```
    Header Authorization:
    {
        Authorization: "8uP9dv0czfTLY8WEma1fZyBYLzUedsX.iwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Successful response (code 200 - OK):
    {
        "user": {
            "id": "Id from the user",
            "first_name": "First name from the user",
            "last_name": "Last name from the user",
            "email": "Email from the user",
            "password": "Password from the user"
        }
    }

    Response with errors (code 401 - UNAUTHORIZED):
    {
        "msg": "Missing Authorization Header"
    }
    ```
    """
    @jwt_required(locations=["headers"], optional=False)
    @is_token_blacklisted
    def get(self, user_id: str):
        if not user_id:
            return {"error": "Not data in URL"}, 400
        try:
            user_exists = user_service.get_user_by_id(user_id)
            return {"user": user_exists}, 200
        except UserNotFoundException as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400
        

class UserLogoutResource(Resource):
    """
    Example:

    GET: /users/logout
    ```
    Header Authorization:
    {
        Authorization: "8uP9dv0czfTLY8WEma1fZyBYLzUedsX.iwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Successful response (code 200 - OK):
    {
        "msg": "Logout succesfully"
    }

    Response with errors (code 400 - BAD REQUEST):
    {
        "msg": "Missing Authorization Header"
    }
    ```
    """
    @jwt_required(locations=["headers"], optional=False)
    def post(self):
        try:
            token_jti = get_jwt().get("jti")
            blacklist_token = token_service.blacklist_token(token_jti)
            return {"msg": "Logout succesfully"}, 200
        except TokenAlreadyBlacklisted as error:
            return {"error": (str(error))}, 400
        except Exception as error:
            return {"error": (str(error))}, 400