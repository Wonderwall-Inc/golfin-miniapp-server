"""
JWTBearer is a subclass of HTTPBearer responsible for handling JWT (JSON Web Token) authentication 
in FastAPI applications.

Args:
    auto_error (bool, optional): Flag to automatically raise an HTTPException 
    if authentication fails
    Defaults to True.

Attributes:
    kid_to_jwk (Dict[str, Dict[str, Any]]): A dictionary that maps the key ID (kid) to the 
    corresponding JSON Web Key (JWK) from the JWKS.

Methods:
    __init__(self, auto_error: bool = True): Initializes the JWTBearer class.
    get_jwks(self, url: str): Gets the JSON Web Key Set (JWKS) from the configured URL.
    verify_jwk_token(self, jwt_credentials: JWTAuthorizationCredentials) -> bool: Verifies the JWT by
    retrieving the corresponding public key from the JWKS and validating the signature.
    __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]: Overrides the __call__ method
    to extract the JWT credentials from the request and validate them.
"""
from typing import Optional

import requests
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from cachetools import cached, TTLCache
from core.models import JWTAuthorizationCredentials
from core.auth_credential import jwks_url


class JWTBearer(HTTPBearer):
    """
    JWTBearer is a subclass of HTTPBearer responsible for handling JWT (JSON Web Token) authentication
    in FastAPI applications.

    Args: jwks (JWKS): The JSON Web Key Set (JWKS) used for verifying the authenticity of the JWT.
    auto_error (bool, optional): Flag to automatically raise an HTTPException if authentication fails
    Defaults to True.

    Attributes: kid_to_jwk (Dict[str, Dict[str, Any]]): A dictionary that maps the key ID (kid) to the
    corresponding JSON Web Key (JWK) from the JWKS.
    """

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        jwks = self.get_jwks(jwks_url)
        self.kid_to_jwk = {jwk["kid"]: jwk for jwk in jwks.keys}

    @cached(TTLCache(maxsize=1, ttl=3600))
    def get_jwks(self, url: str):
        """
        Gets the JSON Web Key Set (JWKS) from the configured URL.
        The JWKS is cached using a TTLCache for performance.

        Returns: JWKS: The JSON Web Key Set.
        """
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()

    def verify_jwk_token(self, jwt_credentials: JWTAuthorizationCredentials) -> bool:
        """
        Verifies the JWT by retrieving the corresponding public key from the JWKS and validating the
        signature.

        Args: jwt_credentials (JWTAuthorizationCredentials): The JWT credentials to be verified.
        Returns: bool: True if the JWT is valid, False otherwise.
        Raises: HTTPException: If the JWK public key is not found.
        """
        try:
            public_key = self.kid_to_jwk[jwt_credentials.header["kid"]]
        except KeyError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="JWK public key not found"
            )

        key = jwk.construct(public_key)
        decoded_signature = base64url_decode(jwt_credentials.signature.encode())

        return key.verify(jwt_credentials.message.encode(), decoded_signature)

    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]:
        """
        Overrides the __call__ method to extract the JWT credentials from the request and validate them.

        Args: request (Request): The incoming request.
        Returns: Optional[JWTAuthorizationCredentials]: The validated JWT credentials if authentication is
        successful, None otherwise.
        Raises: HTTPException: If the authentication method is not 'Bearer' or if the JWT is invalid.
        """
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Wrong authentication method"
                )

            jwt_token = credentials.credentials

            message, signature = jwt_token.rsplit(".", 1)

            try:
                jwt_credentials = JWTAuthorizationCredentials(
                    jwt_token=jwt_token,
                    header=jwt.get_unverified_header(jwt_token),
                    claims=jwt.get_unverified_claims(jwt_token),
                    signature=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JSON Web Key invalid"
                )

            if not self.verify_jwk_token(jwt_credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JSON Web Key invalid"
                )

            return jwt_credentials
