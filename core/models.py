"""
This file contains the models used in common core application.
"""
from typing import Dict, List
from pydantic import BaseModel


JWK = Dict[str, str]


class JWKS(BaseModel):
    """JWKS model."""

    keys: List[JWK]


class JWTAuthorizationCredentials(BaseModel):
    """
    Represents the credentials required for JWT authorization.

    Args:
        jwt_token (str): A string representing the JWT token.
        header (Dict[str, str]): A dictionary representing the header of the JWT token.
        claims (Dict[str, str]): A dictionary representing the claims of the JWT token.
        signature (str): A string representing the signature of the JWT token.
        message (str): A string representing an additional message associated with the credentials.
    """

    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str
