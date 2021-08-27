from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import RemoteConfig, get_config
from app.models.user import UserPublic
from app.patches.azure_ad_verify_token import verify_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[UserPublic]:
    if token is None:
        return None
    else:
        try:
            payload = verify_jwt(
                token=token,
                valid_audiences=[get_config(RemoteConfig.AZURE_AD_APP_ID)],
                issuer=get_config(RemoteConfig.AZURE_AD_ISSUER),
                jwks_uri=get_config(RemoteConfig.AZURE_AD_JWKS_URI),
            )

            sub = payload.get("sub", "")
            name = payload.get("name", "")
            given_name = payload.get("given_name", "")
            family_name = payload.get("family_name", "")
            member_id = payload.get("extension_MemberID", "")
            group_number = payload.get("extension_GroupNumber", "")
            dob = payload.get("extension_DateofBirth", "")

            data = {
                "id": sub,
                "displayName": name,
                "employeeId": "",
                "given_name": given_name,
                "locale": "",
                "family_name": family_name,
                "email": "",
                "date_of_birth": dob,
                "member_id": member_id,
                "group_number": group_number,
            }
            return UserPublic(**data)
        except:  # noqa
            return None
