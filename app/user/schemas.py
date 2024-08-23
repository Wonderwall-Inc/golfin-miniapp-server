"""Users Pydantic Schemas"""

from pydantic import BaseModel


class UserSchema(BaseModel):
    """User Base Schema"""


class UserUpdateDetailsSchema(BaseModel):
    """User Update Detail Schema"""


class UserDetailsSchema(BaseModel):
    """User Display Schema"""


class UserAccessRequestSchema(BaseModel):
    """User Access Request Schema"""


class UserAccessResponseSchema(BaseModel):
    """User Access Response Schema"""


class UserDetailsResponseSchema(BaseModel):
    """User Details Response Schema"""

    user_details: UserDetailsSchema


class UserUpdateSchema(BaseModel):
    """User Update Schema"""
