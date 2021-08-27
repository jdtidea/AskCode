from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from authlib.jose import jwt

from app.core.config import RemoteConfig, get_config


class StargateEnv(str, Enum):
    STAGE = "STAGE"
    PROD = "PROD"


def create_access_token(
    stargate_env: Optional[StargateEnv] = StargateEnv.PROD,
    payload: Optional[dict] = {},
    expires_delta: Optional[timedelta] = None,  # noqa
) -> str:
    to_encode = payload.copy()

    jwt_key_config = (
        RemoteConfig.AO_SG_JWT_KEY_PROD
        if stargate_env is StargateEnv.PROD
        else RemoteConfig.AO_SG_JWT_KEY_STAGE
    )
    jwt_secret_config = (
        RemoteConfig.AO_SG_JWT_SECRET_PROD
        if stargate_env is StargateEnv.PROD
        else RemoteConfig.AO_SG_JWT_SECRET_STAGE
    )

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=40)

    to_encode.update({"exp": expire, "iss": get_config(jwt_key_config)})
    header = {"alg": "HS256"}

    encoded_jwt = jwt.encode(header, to_encode, get_config(jwt_secret_config))

    return encoded_jwt.decode("utf-8")
