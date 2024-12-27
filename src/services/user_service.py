import json
from bson import ObjectId
from pymongo.results import InsertOneResult
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)

from repositories.user_repository import UserRepository
from entities.user_model import UserModelRegister, UserModel
from exceptions.user_exceptions import (
    UserNotFoundException,
    UserAlreadyExists,
    PasswordDontMatch
)

class UserService:
    def __init__(self):
        """
        Initializes the UserService instance.

        Attributes:
        ----------
        user_repository : a instance from "UserRepository"
        """
        self.user_repository = UserRepository()

    def get_user_id_requeted(self, user_identity_dict: dict):
        user_id = user_identity_dict.get("id")
        return user_id
    
    def _model_dump_json(self, user_data_dict: dict, exclude_password: bool):
        """
        Serializes the UserModel into JSON format, with an option to exclude the password.

        Args:
        ----
        user_data_dict (dict): The user data to serialize.
        exclude_password (bool, optional): Whether to exclude the password field. Defaults to True.

        Returns:
        -------
        str: JSON string of the user data.
        """
        user_model = UserModel.model_validate(user_data_dict)
        if exclude_password:
            return user_model.model_dump_json(exclude={"password"})
        return user_model.model_dump_json()
    
    def _format_model_in_json(self, user_data):
        return json.loads(user_data)
        
    async def _hash_password(self, password: str) -> str:
        """
        Generates a hashed password using the scrypt algorithm.
        
        Args:
        password (str): Plain text password to be hashed.
        
        Returns:
        str: The hashed password.
        """
        return generate_password_hash(password)

    async def _verify_password(self, password_hashed: str, password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password.
        
        Args:
        ----
        password (str): Plain text password to verify.
        password_hashed (str): Hashed password to compare against.
        
        Returns:
        -------
        bool: True if the password matches, False otherwise.
        """
        passwords_equals = check_password_hash(password_hashed, password)
        if not passwords_equals:
            raise PasswordDontMatch
        return passwords_equals
    
    async def _process_passwords(self, password: str, confirm_password: str) -> str:
        """
        Hashes the password if it matches the confirmation, raises error otherwise.
        """
        if password != confirm_password:
            raise PasswordDontMatch()
        return await self._hash_password(password)
    
    async def _check_user_exists_by_id(self, user_id: str):
        """
        Check if there is any record with this user id.

        Args:
        ----
        user_id (str): Id from the user to verify.
        
        Returns:
        -------
        dict: A dict with the all information from the user if exists, False otherwise.
        """
        user_id_formated = ObjectId(user_id)
        user_instance = await self.user_repository.get_user_by_id(user_id_formated)
        return user_instance if user_instance else False
    
    async def _check_user_exists_by_email(self, email: str):
        """
        Check if there is any record with this email.
        
        Args:
        user_id (str): Id from the user to verify.
        
        Returns:
        dict: A dict with the all information from the user if exists, False otherwise.
        """
        user_instance = await self.user_repository.get_user_by_email(email)
        return user_instance if user_instance else False
    
    async def get_user_by_id(self, user_id: str) -> UserModel:
        """
        Retrieves a user by their ID and returns a UserModel instance with their details.
        
        Args:
        user_id (str): The ID of the user to retrieve.
        
        Returns:
        UserModel: Instance with the user's details, or None if the user is not found.
        """
        user = await self._check_user_exists_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        
        user_model_dump_json = self._model_dump_json(user, True)
        user_format_json = self._format_model_in_json(user_model_dump_json)
        return user_format_json

    async def get_user_by_email(self, user_email: str) -> UserModel:
        """
        Retrieves a user by their email and returns a UserModel instance with their details.
        
        Args:
        user_email (str): The email of the user to retrieve.
        
        Returns:
        UserModel: Instance with the user's details, or None if the user is not found.
        """
        user = await self._check_user_exists_by_email(user_email)
        if user:
            raise UserAlreadyExists()
        
        user_model_dump_json = self._model_dump_json(user, True)
        user_format_json = self._format_model_in_json(user_model_dump_json)
        return user_format_json

    async def create_user(self, data: dict) -> InsertOneResult:
        """
        Creates a new user with the provided details, ensuring the email is not already registered.
        
        Args:
        ----
        data (dict): dict with all fields from the models.
        
        Returns:
        -------
        UserModelRegister: Instance of the newly created user.
        """
        users_exists = await self._check_user_exists_by_email(data["email"])
        if users_exists:
            raise UserAlreadyExists()
        
        user_model_register = UserModelRegister.model_validate(data)

        password_hashed = await self._process_passwords(data["password"], data["confirm_password"])

        user_model_register_dict = user_model_register.model_dump()
        user_model_register_dict.pop("confirm_password")
        user_model_register_dict["password"] = password_hashed

        user_instance_model = UserModel.model_validate(user_model_register_dict)
        user_created = self.user_repository.create_user(user_instance_model)
        return user_created.inserted_id

    async def authenticate_user(self, data: dict) -> UserModel:
        """
        Authenticates a user by their email and password.
        
        Args:
        ----
        email (str): The email of the user attempting to authenticate.
        password (str): The plain text password provided by the user.
        
        Returns:
        -------
        UserModel: The authenticated user instance if credentials are valid, None otherwise.
        """
        user = await self._check_user_exists_by_email(data["email"])
        if not user:
            raise UserNotFoundException()
        await self._verify_password(user["password"], data["password"])
        user_model_dump_json = self._model_dump_json(user, True)
        return self._format_model_in_json(user_model_dump_json)
    
    async def update_user(self, token: dict, data: dict):
        """
        Update the current data from the user.

        Args:
        ----
        token (dict): A dictionary with user token information.
        data (dict): A dictionary with the new data from the user.
        
        Returns:
        -------
        UpdateResult: A instance from UpdateResult of Pymongo.
        """
        user_id = self.get_user_id_requeted(token)
        if not await self._check_user_exists_by_id(user_id):
            raise UserNotFoundException()
        return await self.user_repository.update_user(user_id, data)
