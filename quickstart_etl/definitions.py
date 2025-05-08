from pathlib import Path

from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    link_code_references_to_git,
    load_assets_from_package_module,
    with_source_code_references,
)
from dagster._core.definitions.metadata.source_code import AnchorBasedFilePathMapping

from . import assets
from .assets import airbyte
from . import resources

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

my_assets = with_source_code_references(
    [
        *load_assets_from_package_module(assets),
    ]
)

my_assets = link_code_references_to_git(
    assets_defs=my_assets,
    git_url="https://github.com/dagster-io/dagster/",
    git_branch="master",
    file_path_mapping=AnchorBasedFilePathMapping(
        local_file_anchor=Path(__file__).parent,
        file_anchor_path_in_repository="examples/quickstart_etl/quickstart_etl/",
    ),
)

defs = Definitions(
    assets=my_assets,
    resources={
        "redshift": resources.redshift,
        "airbyte": resources.airbyte
    },
    # schedules=[daily_refresh_schedule],
    # jobs=[airbyte.sync_platform_users_job],
    jobs=[airbyte.get_airbyte_token_job]
)
