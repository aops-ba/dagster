import dagster
from dagster import EnvVar
from dagster_airbyte import (
    build_airbyte_assets,
    load_assets_from_airbyte_instance,
    airbyte_sync_op,
)
from .. import resources
import requests

connection_id = "8d000892-ce40-4ab5-bb3c-72ef6896ac61"
workspace_id = "f8687182-1367-4508-bf2e-59b3fa153b5f"

# airbyte_assets = build_airbyte_assets(
#     connection_id=connection_id,
#     destination_tables=["ab_dev_users"]
# )

# sync_platform_users = airbyte_sync_op.configured({
#     "connection_id": connection_id,
# }, name="sync_platform_users")

# @dagster.job(resource_defs={"airbyte": resources.airbyte})
# def sync_platform_users_job():
#     sync_platform_users()

BASE_URL = "http://{host}:{port}/api/v1/".format(
    host=EnvVar("AIRBYTE_HOST").get_value(),
    port=EnvVar.int("AIRBYTE_PORT").get_value()
)

@dagster.op
def get_airbyte_token():
    response = requests.post(
        BASE_URL + "applications/token",
        json={
            "client_id": EnvVar("AIRBYTE_CLIENT_ID").get_value(),
            "client_secret": EnvVar("AIRBYTE_CLIENT_SECRET").get_value(),
        }
    )
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Failed to get token")
    
@dagster.job
def get_airbyte_token_job():
    get_airbyte_token()

# airbyte_assets = load_assets_from_airbyte_instance(resources.airbyte, workspace_id=workspace_id)
# defs = dagster.Definitions(
#     assets=[airbyte_assets]
# )
# defs = dagster.Definitions(
#     jobs={
#         "sync_platform_users": sync_platform_users
#     }
# )
