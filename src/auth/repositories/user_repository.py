from bson import ObjectId
from pymongo.results import InsertOneResult, UpdateResult

from database.db import Database
from auth.models.user_model import UserModel

class UserRepository:
    def __init__(self):
        """
        Initializes the UserDao instance.

        Attributes:
        ----------
        __database: Database
            An instance of the Database class, used to interact with the
            methods of this class.
        user_collection: An instance of the method "users_collection" from t
            he database to interact with the respective collection.
        """
        self.__database = Database()
        self.user_collection = self.__database.users_collection()

    def create_user(self, user_instance_model: UserModel) -> InsertOneResult:
        """
        Inserts the user's data into the corresponding collection and returns its ID.

        Args:
        ----
        user_data (UserModel): Instance from the model

        Returns:
        -------
        UserModel: Insert result, including the ID of the new document.
        """
        user_data_dict = user_instance_model.model_dump(by_alias=True)
        user_created = self.user_collection.insert_one(user_data_dict)
        return user_created

    def get_user_by_id(self, user_id: str) -> dict:
        """
        Returns a instance from the user

        Args:
        user_id (str): User ID to search

        Returns:
        UserModel: User model instance
        """
        user_dict_id = {"_id": ObjectId(user_id)}
        user_data = self.user_collection.find_one(user_dict_id)
        return user_data
    
    def get_user_by_email(self, user_email: str) -> dict:
        """
        Return a instance from the user's

        Args:
        user_email (str): User email to search

        Returns:
        UserModel: user's information in model instance
        """
        user_dict_email = {"email": user_email}
        user_data = self.user_collection.find_one(user_dict_email)
        return user_data

    def update_user(self, user_id: str, user_model_instance: UserModel) -> UpdateResult:
        """  
        Replaces new information in a record where it matches the ID entered.

        Args:
        ----
        user_id (str): ID from the user.
        user_model_instance (UserModel): Instance from the model

        Returns:
        -------
        UpdateResult: a instance from the user with the data updated
        """
        user_dict_id = {"_id": ObjectId(user_id)}
        user_new_data_dict = user_model_instance.model_dump(by_alias=True)
        user_update = self.user_collection.update_one(user_dict_id, user_model_instance)
        return user_update