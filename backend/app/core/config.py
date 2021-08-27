import os
from enum import Enum

from azure.appconfiguration import AzureAppConfigurationClient
from starlette.config import Config, Environ

config = Config()
PROJECT_NAME = "AskOptum"
VERSION = "1.0.0"
ALLOWED_HOST_ORIGINS = None
REQUEST_TIMEOUT = 10.0

APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
    "InstrumentationKey=00000000-0000-0000-0000-000000000000",
)


class RemoteConfigVersion:
    def __init__(self, version: int = 0):
        self.version = version


class RemoteConfig(Enum):
    AO_SG_JWT_KEY_PROD = "AO_SG_JWT_KEY_PROD"
    AO_SG_JWT_KEY_STAGE = "AO_SG_JWT_KEY_STAGE"
    AO_SG_JWT_SECRET_PROD = "AO_SG_JWT_SECRET_PROD"
    AO_SG_JWT_SECRET_STAGE = "AO_SG_JWT_SECRET_STAGE"
    AVA_BNE_URL = "AVA_BNE_URL"
    AVA_BNE_URL_STAGE = "AVA_BNE_URL_STAGE"
    AVA_VCM_URL = "AVA_VCM_URL"
    AZURE_AD_APP_ID = "AZURE_AD_APP_ID"
    AZURE_AD_ISSUER = "AZURE_AD_ISSUER"
    AZURE_AD_JWKS_URI = "AZURE_AD_JWKS_URI"
    DEMO_USERS = "DEMO_USERS"
    HEALTH_URL = "HEALTH_URL"
    UHG_DOMAINS_URL = "UHG_DOMAINS_URL"
    LOG_LEVEL = "LOG_LEVEL"
    DOMAIN_THRESHOLD = "DOMAIN_THRESHOLD"
    CONFIG_VERSION = "CONFIG_VERSION"
    RANKING_URL = "RANKING_URL"
    AZURE_STORAGE_CONNECTION_STRING = "AZURE_STORAGE_CONNECTION_STRING"
    SKILL_REGISTRY_BLOB_CONTAINER_NAME = "SKILL_REGISTRY_BLOB_CONTAINER_NAME"
    SKILL_REGISTRY_BLOB_PATH = "SKILL_REGISTRY_BLOB_PATH"
    RANKING_BLOB_CONTAINER_NAME = "RANKING_BLOB_CONTAINER_NAME"
    RANKING_BLOB_PATH = "RANKING_BLOB_PATH"


remote_config_version = RemoteConfigVersion()


def get_config(key: RemoteConfig) -> str:
    return config.get(key.value, cast=str, default="")


def initialize_environment() -> None:
    client = AzureAppConfigurationClient.from_connection_string(
        os.getenv("APP_CONFIG_CONNECTION_STRING", "")
    )
    env = Environ()
    config_version = int(
        client.get_configuration_setting(RemoteConfig.CONFIG_VERSION).value
    )
    if config_version > remote_config_version.version:
        remote_config_version.version = config_version
        # TODO: Prefix all config settings with AO_* and filter
        settings = client.list_configuration_settings()

        for setting in settings:
            env.__setitem__(setting.key, setting.value)

    config.environ = env
