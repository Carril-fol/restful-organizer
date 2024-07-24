from auth.repositories.token_repository import TokenRepository
from auth.models.token_model import TokenModel
from auth.exceptions.token_exceptions import TokenAlreadyBlacklisted


class TokenService(object):
    def __init__(self):
        """
        Initializes the TokenService instance.

        Attributes:
        ----------
        token_dao: a instance from "TokenRepository"
        """
        self.token_repository = TokenRepository()

    def check_token_if_blacklisted(self, token_jti: str):
        """
        Check if there is any record with this JTI.

        Args:
        ----
        token_jti (str): JTI from the token.
        
        Returns:
        -------
        bool:
        """
        token = self.token_repository.get_token_by_jti(token_jti)
        return True if token else False
    
    def blacklist_token(self, token_jti: str):
        """
        Create a new record with the token identifier.
        
        Args:
        ----
        token_jti (str): The identifier of the token to save .
        
        Returns:
        -------
        InsertOneResult: Instance of pymongo data inserted.
        """
        token_is_blacklisted = self.check_token_if_blacklisted(token_jti)
        if token_is_blacklisted:
            raise TokenAlreadyBlacklisted()
        token_model_instance = TokenModel(jti=token_jti)
        token_blacklist_instance = self.token_repository.blacklist_token(token_model_instance)
        return token_blacklist_instance