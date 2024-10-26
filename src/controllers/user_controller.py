# Imports
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from services.user_service import UserService
from services.token_service import TokenService
from exceptions.user_exceptions import UserNotFoundException
from decorators.user_decorator import is_token_blacklisted

# Blueprint
auth_blueprint = Blueprint("users", __name__, url_prefix="/users/api/v1")

# Services
user_service = UserService()
token_service = TokenService()

@auth_blueprint.route("/register", methods=["POST"])
async def register():
    """
    Example:

    POST: /users/api/v1/register

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
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON in request"}, 400       
    try:
        new_user = await user_service.create_user(data)
        user_json = await user_service.get_user_by_id(new_user)
        access_token = create_access_token(user_json)
        return {"msg": "User created", "user": user_json, "access_token": access_token}, 201
    except Exception as error:
        return {"error": (str(error))}, 400 


@auth_blueprint.route("/login", methods=["POST"])
async def login():
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
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON in request"}, 400
    try:
        user_exists = await user_service.authenticate_user(data)
        refresh_token = create_refresh_token(user_exists)
        access_token = create_access_token(user_exists)
        tokens = {
            "access_token": access_token, 
            "refresh_token": refresh_token
        }
        return {"msg": "Login succefully", "tokens": tokens}, 200
    except UserNotFoundException as error:
        return {"error": (str(error))}, 404
    except Exception as error:
        return {"error": (str(error))}, 400
    

@jwt_required()
@is_token_blacklisted
@auth_blueprint.route("/detail", methods=["GET"])
async def detail_user_requested():
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
    user_identity = get_jwt_identity()
    try:
        user_exists = await user_service.get_user_by_id(user_identity)
        return {"user": user_exists}, 200
    except UserNotFoundException as error:
        return {"error": (str(error))}, 404
    except Exception as error:
        return {"error": (str(error))}, 400


@jwt_required(optional=False)
@auth_blueprint.route("/logout", methods=["POST"])
async def logout():
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
    try:
        token = get_jwt()
        blacklist_token = await token_service.blacklist_token(token)
        return {"msg": "Logout succesfully"}, 200
    except Exception as error:
        return {"error": (str(error))}, 400


@jwt_required(verify_type=True, refresh=True)
@auth_blueprint.route("/refresh", methods=["POST"])
def refresh_token():
    """
    Example:

    POST: /users/api/v1/refresh
    ```
    Header data:
    {
        "Authorization": "8uP9dv0czfTLY8WEma1fZyBYLzUedsXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Successful response (code 200 - OK):
    {
        "access_token": "8aP9dv0czfTLY8WEma1fZyBYLzUedsXdsdp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }
    ```
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return {"access_token": new_access_token}, 200