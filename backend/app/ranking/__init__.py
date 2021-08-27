import pickle

from azure.storage.blob import BlobServiceClient

from app.core.config import RemoteConfig, get_config

map_to_name = {}
map_to_org_key = {}
syn_df = {}
stopwords = {}
key_replace = {}


def initialize_ranking() -> None:
    global map_to_name
    global map_to_org_key
    global syn_df
    global stopwords
    global key_replace
    blob_service_client = BlobServiceClient.from_connection_string(
        get_config(RemoteConfig.AZURE_STORAGE_CONNECTION_STRING)
    )
    blob_client = blob_service_client.get_blob_client(
        container=get_config(RemoteConfig.RANKING_BLOB_CONTAINER_NAME),
        blob=get_config(RemoteConfig.RANKING_BLOB_PATH),
    )
    data = blob_client.download_blob().readall()

    ranking_map = pickle.loads(data)
    map_to_name = ranking_map["map_to_name"]
    map_to_org_key = ranking_map["map_to_org_key"]
    syn_df = ranking_map["syn_df"]
    stopwords = ranking_map["stopwords"]
    key_replace = ranking_map["key_replace"]
