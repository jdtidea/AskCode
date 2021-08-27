from typing import List

import yaml
from azure.storage.blob import BlobServiceClient
from pydantic import parse_obj_as

from app.core.config import RemoteConfig, get_config
from app.models.skills import SkillMeta, SkillRegistry

registry = SkillRegistry(skills=[])
registry_map = {}


def get_registry_map():
    return registry_map


def initialize_skill_registry() -> None:
    global registry_map
    global registry
    blob_service_client = BlobServiceClient.from_connection_string(
        get_config(RemoteConfig.AZURE_STORAGE_CONNECTION_STRING)
    )
    blob_client = blob_service_client.get_blob_client(
        container=get_config(RemoteConfig.SKILL_REGISTRY_BLOB_CONTAINER_NAME),
        blob=get_config(RemoteConfig.SKILL_REGISTRY_BLOB_PATH),
    )
    data = blob_client.download_blob().readall()

    skills = parse_obj_as(List[SkillMeta], yaml.safe_load(data).get("skills"))
    new_registry_map = {}
    for skill in skills:
        for entity in skill.entities:
            if entity in new_registry_map:
                new_registry_map[entity].append(skill)
            else:
                new_registry_map[entity] = [skill]
    registry.skills = skills
    registry_map = new_registry_map
