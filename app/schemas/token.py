from pydantic import BaseModel

class TokenCreate(BaseModel):
    """
    Schema representing the tokens returned after authentication.

    Attributes:
        access_token (str): JWT access token.
        refresh_token (str): Refresh token to obtain new access tokens.
        token_type (str): Type of the token, usually "bearer".
    """
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema containing token payload data, typically used for validation.

    Attributes:
        email (str | None): Email extracted from the token, optional.
    """
    email: str | None = None


class TokenRefresh(BaseModel):
    """
    Schema used to request a new access token via a refresh token.

    Attributes:
        refresh_token (str): The refresh token string.
    """
    refresh_token: str
