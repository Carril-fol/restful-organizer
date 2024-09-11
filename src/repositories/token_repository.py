from pymongo.results import InsertOneResult
from database.db import Database

from models.token_model import TokenModel


class TokenRepository(object):
    def __init__(self):
        """
        Initializes the TokenRepository instance.

        Attributes:
        ----------
        __database: Database
            An instance of the Database class, used to interact with their methods.
        token_collection: An instance of the method "tokens_collection" 
            to interact with their respective collection in the database.
        """
        self.__database = Database()
        self.token_collection = self.__database.tokens_collection()

    def get_token_by_jti(self, token_jti: str):
        """
        Returns a dict from the token

        Args:
        ----
        token_jti (str): JTI from the token

        Returns:
        -------
        dict: A dict with the information from the token
        """
        token_dict = {"jti": token_jti}
        token = self.token_collection.find_one(token_dict)
        return token
    
    def blacklist_token(self, token_model_instance: TokenModel) -> InsertOneResult:
        """
        Inserts the token´s data into the corresponding collection.

        Args:
        ----
        token_model_instance (TokenModel): Instance of the token model with 
        the data to be inserted.
        
        Returns:
        -------
        InsertOneResult: Insert result.
        """
        token_dict_data = token_model_instance.model_dump(by_alias=True)
        token = self.token_collection.insert_one(token_dict_data)
        return token