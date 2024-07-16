from flask import request
from flask_restful import Resource

from extensions import cache
from folders.services.folder_service import FolderService

folder_service = FolderService()

class CreateFolderResource(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {"error", "Missing JSON in the request"}, 400
        try:
            folder_created = folder_service.create_folder(data)
            return {"status": "created", "folder": folder_created}, 201
        except Exception as error:
            return {"error": (str(error))}, 400
        

class GetFoldersByUserIdResource(Resource):

    @cache.cached(timeout=50)
    def get(self, user_id: str):
        try:
            folders = folder_service.get_folders_by_user_id(user_id)
            return {"folders": folders}, 200
        except Exception as error:
            return {"error": (str(error))}, 400


class UpdateFolderResource(Resource):

    def put(self, folder_id: str):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in the request"}
        try:
            folder_instance_update = folder_service.update_folder(folder_id, data)
            return {
                "status": "Updated",
                "folder": folder_instance_update
            }, 200
        except Exception as error:
            return {"error": (str(error))}, 400
        

class DeleteFolderResource(Resource):

    def delete(self, folder_id: str):
        try:
            folder_delete = folder_service.delete_folder(folder_id)
            return {"status": "Deleted"}, 200
        except Exception as error:
            return {"error": (str(error))}, 400