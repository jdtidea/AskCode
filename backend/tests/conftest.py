import json
import os
import re

import docker as pydocker
import pytest
from asgi_lifespan import LifespanManager
from azure.appconfiguration._azure_appconfiguration_client import (
    AzureAppConfigurationClient,
    ConfigurationSetting,
)
from azure.storage.blob import BlobClient, BlobServiceClient, StorageStreamDownloader
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_httpx import HTTPXMock

from app.core.config import RemoteConfig
from app.models.skills import Input
from app.models.user import UserPublic


@pytest.fixture(scope="session")
def docker() -> pydocker.APIClient:
    # base url is the unix socket we use to communicate with docker
    return pydocker.APIClient(base_url="unix://var/run/docker.sock", version="auto")


# Create a new application for testing
@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


class MockAzureAppConfigurationClient:
    @staticmethod
    def get_configuration_setting(key):
        if key == RemoteConfig.CONFIG_VERSION:
            return ConfigurationSetting(key=RemoteConfig.CONFIG_VERSION, value="1")
        if "URL" in str(key):
            return ConfigurationSetting(key=key, value="https://" + key)
        return ConfigurationSetting(key=key, value=key)

    @staticmethod
    def list_configuration_settings():
        settings = []
        for config in RemoteConfig:
            settings.append(
                ConfigurationSetting(
                    key=config.name,
                    value=config.value
                    if "URL" not in config.value
                    else f"https://{config.value}",
                )
            )
        return settings


@pytest.fixture(autouse=True)
def mock_app_config(monkeypatch):
    client = MockAzureAppConfigurationClient()

    def mock_from_connection_string(connection_string):
        return client

    def mock_get_configuration_setting(key):
        return client.get_configuration_setting(key)

    def mock_list_configuration_settings():
        return client.list_configuration_settings()

    monkeypatch.setattr(
        AzureAppConfigurationClient,
        "from_connection_string",
        mock_from_connection_string,
    )
    monkeypatch.setattr(
        AzureAppConfigurationClient,
        "get_configuration_setting",
        mock_get_configuration_setting,
    )
    monkeypatch.setattr(
        AzureAppConfigurationClient,
        "list_configuration_settings",
        mock_list_configuration_settings,
    )


class MockBlobServiceClient:
    @staticmethod
    def get_blob_client(container, blob):
        return MockBlobClient(container)


class MockBlobClient:
    def __init__(self, container_name: str):
        self.container_name = container_name
        if container_name == RemoteConfig.SKILL_REGISTRY_BLOB_CONTAINER_NAME.value:
            self.stream_downloader = MockStorageStreamDownloader(
                "data/skill_registry_mock.yaml"
            )
        elif container_name == RemoteConfig.RANKING_BLOB_CONTAINER_NAME.value:
            self.stream_downloader = MockStorageStreamDownloader(
                "data/ranking_mock.pickle"
            )
        else:
            self.stream_downloader = MockStorageStreamDownloader("data/default.txt")

    def download_blob(self):
        return self.stream_downloader


class MockStorageStreamDownloader:
    def __init__(self, file: str):
        self.file = file

    def readall(self):
        with open(os.path.join(os.path.dirname(__file__), self.file), "rb") as f:
            return f.read()


@pytest.fixture(autouse=True)
def mock_blob_service(monkeypatch):
    blob_service_client = MockBlobServiceClient()

    def mock_from_connection_string(connection_string):
        return blob_service_client

    def mock_get_blob_client(container, blob):
        return MockBlobClient(container)

    monkeypatch.setattr(
        BlobServiceClient,
        "from_connection_string",
        mock_from_connection_string,
    )
    monkeypatch.setattr(
        BlobServiceClient,
        "get_blob_client",
        mock_get_blob_client,
    )


# Mock all known http requests
@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def mock_httpx(httpx_mock: HTTPXMock):
    with open(os.path.join(os.path.dirname(__file__), "data/domains_valid.json")) as f:
        domains_data = json.load(f)
    httpx_mock.add_response(
        url=f"https://{RemoteConfig.UHG_DOMAINS_URL.value}",
        json=domains_data,
    )
    with open(os.path.join(os.path.dirname(__file__), "data/bne_valid.json")) as f:
        bne_data = json.load(f)
    httpx_mock.add_response(
        url=f"https://{RemoteConfig.AVA_BNE_URL.value}", json=bne_data
    )
    with open(
        os.path.join(os.path.dirname(__file__), "data/vcm_valid_response.json")
    ) as f:
        vcm_data = json.load(f)
    httpx_mock.add_response(
        url=f"https://{RemoteConfig.AVA_VCM_URL.value}", json=vcm_data
    )
    with open(
        os.path.join(os.path.dirname(__file__), "data/health_library_valid.json")
    ) as f:
        health_library_data = json.load(f)
    httpx_mock.add_response(
        url=re.compile("https://health_url*"),
        json=health_library_data,
    )
    with open(
        os.path.join(os.path.dirname(__file__), "data/ranking_response.json")
    ) as f:
        ranking_data = json.load(f)
    httpx_mock.add_response(
        url=re.compile("https://ranking_url*"),
        json=ranking_data,
    )


@pytest.fixture
def assert_all_responses_were_requested() -> bool:
    return False


# Don't mock our test HTTP server
@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]


default_user = {
    "id": "00000000-0000-0000-0000-000000000000",
    "displayName": "AYLISSA PEGUERO",
    "given_name": "AYLISSA",
    "family_name": "PEGUERO",
    "email": "ap@optum.com",
    "date_of_birth": "01/02/1992",
    "member_id": "909854131",
    "group_number": "0907746",
    "set_number": "001ACIS",
}


@pytest.fixture
def mock_user() -> UserPublic:
    return UserPublic(**default_user)


@pytest.fixture
def mock_input(mock_user) -> Input:
    return Input(raw_query="back pain", identity=mock_user)
