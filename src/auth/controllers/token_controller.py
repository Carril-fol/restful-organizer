from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from auth.services.token_service import TokenService

token_service = TokenService()

class RefreshTokenResource(Resource):

    @jwt_required(locations=["headers"], verify_type=True, refresh=True)
    def post(self):
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