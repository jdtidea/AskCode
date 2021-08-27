from datetime import datetime, timedelta

from pydantic import EmailStr

from app.models.core import CoreModel


class JWTMeta(CoreModel):
    iss: str = "askoptum"
    aud: str = "test"
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=1))


class JWTCreds(CoreModel):
    """How we'll identify users"""

    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """


class AccessToken(CoreModel):
    access_token: str
    token_type: str
