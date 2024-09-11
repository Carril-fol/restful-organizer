import json
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.results import InsertOneResult

from repositories.user_repository import UserRepository
from models.user_model import UserModelRegister, UserModel
from exceptions.user_exceptions import *

class UserService:
    def __init__(self):
        """
        Initializes the UserService instance.

        Attributes:
        ----------
        user_repository : a instance from "UserRepository"
        """
        self.user_repository = UserRepository()

    def get_user_id_requeted(self, user_data_from_token: dict):
        user_id = user_data_from_token.get("id")
        return user_id
        
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
        return check_password_hash(password_hashed, password)

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
        user_instance = await self.user_repository.get_user_by_id(user_id)
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

    async def get_user_by_id(self, user_identity: dict) -> UserModel:
        """
        Retrieves a user by their ID and returns a UserModel instance with their details.
        
        Args:
        user_id (str): The ID of the user to retrieve.
        
        Returns:
        UserModel: Instance with the user's details, or None if the user is not found.
        """
        user_id = user_identity.get("id")
        user_exists = await self._check_user_exists_by_id(user_id)
        if not user_exists:
            raise UserNotFoundException()
        
        user_model_dump_json = UserModel.model_validate(user_exists).model_dump_json()
        user_format_json = json.loads(user_model_dump_json)
        return user_format_json

    async def get_user_by_email(self, user_email: str) -> UserModel:
        """
        Retrieves a user by their email and returns a UserModel instance with their details.
        
        Args:
        user_email (str): The email of the user to retrieve.
        
        Returns:
        UserModel: Instance with the user's details, or None if the user is not found.
        """
        user_exists = await self._check_user_exists_by_email(user_email)
        if not user_exists:
            raise UserNotFoundException()
        
        user_model_dump_json = UserModel.model_validate(user_exists).model_dump_json()
        user_format_json = json.loads(user_model_dump_json)
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

        user_instance_model_register = UserModelRegister(
            first_name=data["first_name"], 
            last_name=data["last_name"], 
            email=data["email"], 
            password=data["password"],
            confirm_password=data["confirm_password"]
        )

        password_hashed = await self._hash_password(user_instance_model_register.password)
        passwords_check_hashed = await self._verify_password(password_hashed, data["confirm_password"])
        if not passwords_check_hashed:
            raise PasswordDontMatch()

        user_instance_model = UserModel(
            first_name=user_instance_model_register.first_name, 
            last_name=user_instance_model_register.last_name, 
            email=user_instance_model_register.email, 
            password=password_hashed,
        )
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
        user_exists = await self._check_user_exists_by_email(data["email"])
        if not user_exists:
            raise UserNotFoundException()
        
        password_user_stored = user_exists["password"]
        verification_password = await self._verify_password(password_user_stored, data["password"])
        if not verification_password:
            raise PasswordDontMatch()
        
        user_model_dump_json = UserModel.model_validate(user_exists).model_dump_json()
        user_format_json = json.loads(user_model_dump_json)
        return user_format_json