# Imports
from flask import request, Blueprint
from flask_jwt_extended import jwt_required

from utils.extensions import cache
from services.event_service import EventService
from decorators.user_decorator import is_token_blacklisted
from decorators.folder_decorator import is_folder_from_the_user
from decorators.event_decorator import is_event_from_the_user

# Blueprint
event_blueprint = Blueprint("event", __name__, url_prefix="/events/api/v1")

# Service
event_service = EventService()

@is_token_blacklisted
@is_folder_from_the_user
@jwt_required(locations=["headers"], optional=False)
@event_blueprint.route("/create/<folder_id>", methods=["POST"])
def create_event(folder_id: str):
    """
    Example:

    POST: /events/api/v1/create/<folder_id>
    ```
    Application data:
    {
        "name_event": "Name for the event",
        "localization": "Localization from the event",
        "start_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00).
            For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00).",
        "end_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00).
            For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00)."
    }

    Successful response (Code 201 - CREATED):
    {
        "status": "Created",
        "event": {
            "name_event": "Name for the event",
            "folder_id": "Id from the folder",
            "localization": "Localization from the event",
            "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
            "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
        }
    }

    Response with error (Code 404 - NOT FOUND):
    {
        "error": "Folder not found"
    }
    ```
    """
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON in the request"}, 400
    event_created = event_service.create_event(folder_id, data)
    event_detail_created = event_service.detail_event(event_created)
    return {"status": "Created", "event": event_detail_created}, 201

@is_token_blacklisted
@is_event_from_the_user
@cache.cached(timeout=300)
@event_blueprint.route("/detail/<event_id>", methods=["GET"])
def detail_event(event_id: str):
    """
    Example:

    GET: /events/api/v1/<event_id>
    ```
    Successful response (Code 200 - OK):
    {
    "event": {
            "name_event": "Name for the event",
            "folder_id": "Id from the folder",
            "localization": "Localization from the event",
            "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
            "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
        }
    }

    Response with error (Code 404 - NOT FOUND):
    {
        "error": "Event not found"
    }
    ```
    """
    try:
        event_detail = event_service.detail_event(event_id)
        return {"event": event_detail}, 200
    except Exception as error:
        return {"error": (str(error))}, 400

@is_token_blacklisted
@is_event_from_the_user
@jwt_required(locations=["headers"], optional=False)
@event_blueprint.route("/update/<event_id>", methods=["PUT", "PATCH"])
def update_event(event_id: str):
    """
    Example:

    PUT: /events/api/v1/<event_id>
    ```
    Application data:
    {
        "name_event": "Name for the event",
        "folder_id": "Id from the folder",
        "localization": "Localization from the event",
        "start_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00).
                            For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00).",
        "end_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00).
                            For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00)."
    }

    Successful response (Code 200 - OK):
    {
        "event": {
            "name_event": "Name for the event",
            "folder_id": "Id from the folder",
            "localization": "Localization from the event",
            "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
            "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
        }
    }

    Response with error (Code 404 - NOT FOUND):
    {
        "error": "Event not found"
    }

    Response with error (Code 404 - NOT FOUND):
    {
        "error": "Folder not found"
    }
    ```
    """
    try:
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in the request."}, 400
        event_update = event_service.update_event(event_id, data)
        event_detail_updated = event_service.detail_event(event_id)
        return {"status": "Updated", "event": event_detail_updated}, 200
    except Exception as error:
        return {"error": (str(error))}, 400

@is_token_blacklisted
@is_event_from_the_user
@jwt_required(locations=["headers"], optional=False)
@event_blueprint.route("/delete/<event_id>", methods=["DELETE"])
def delete_event(event_id: str):
    """
    Example:

    DELETE: /events/api/v1/<event_id>
    ```
    Successful response (Code 200 - OK):
    {
        "status": "Deleted"
    }

    Response with error (Code 404 - NOT FOUND):
    {
        "error": "Event not found"
    }
    ```
    """
    event_delete = event_service.delete_event(event_id)
    return {"status": "Deleted"}, 200