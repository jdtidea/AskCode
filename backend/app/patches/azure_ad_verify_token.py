import azure_ad_verify_token
import requests
from azure_ad_verify_token.verify import (
    AzureVerifyTokenError,
    InvalidAuthorizationToken,
    verify_jwt,
)

# Store fetched JWKs from B2C in memory as to not fetch on every request
jwk_map = {}


# Patch default get_jwk method as it doesn't cache in-memory
def get_jwk(kid, jwks_uri):
    global jwk_map
    cached_jwk = jwk_map.get(kid, None)
    if cached_jwk is not None:
        return cached_jwk
    resp = requests.get(jwks_uri)
    if not resp.ok:
        raise AzureVerifyTokenError(
            f"Received {resp.status_code} response code from {jwks_uri}"
        )
    try:
        jwks = resp.json()
    except (ValueError, TypeError):
        raise AzureVerifyTokenError(f"Received malformed response from {jwks_uri}")
    # Populate in-memory cache of JWKs
    for jwk in jwks.get("keys"):
        jwk_map[jwk.get("kid")] = jwk
    cached_jwk = jwk_map.get(kid, None)
    if cached_jwk is not None:
        return cached_jwk
    raise InvalidAuthorizationToken("kid not recognized")


azure_ad_verify_token.verify.get_jwk = get_jwk
azure_ad_verify_token.verify.verify_jwt = verify_jwt
