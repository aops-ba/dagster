import dagster as dg
from dagster_fivetran import (
    FivetranWorkspace,
    build_fivetran_assets_definitions,
    DagsterFivetranTranslator,
    FivetranConnectorTableProps
)

fivetran_workspace = FivetranWorkspace(
    account_id=dg.EnvVar("FIVETRAN_ACCOUNT_ID"),
    api_key=dg.EnvVar("FIVETRAN_API_KEY"),
    api_secret=dg.EnvVar("FIVETRAN_API_SECRET")
)

# confusingly, the 'schema' prop in the api response is actually the Connection Name in the Fivetran UI
# this gets mapped to the `name` field in FivetranConnector
class CustomFivetranTranslator(DagsterFivetranTranslator):
    def get_asset_spec(self, props: FivetranConnectorTableProps) -> dg.AssetSpec:
        asset_spec = super().get_asset_spec(props)
        return asset_spec.replace_attributes(
            group_name="fivetran_" + props.name.replace('.', '_'),
        )


select_connectors_not_paused = lambda connector: connector.paused is False
select_connectors_rds = lambda connector: connector.service in { "postgres_rds", "maria_rds" }
select_unpaused_rds = lambda c: select_connectors_not_paused(c) and select_connectors_rds(c)

fivetran_specs = build_fivetran_assets_definitions(
    workspace=fivetran_workspace,
    connector_selector_fn=select_unpaused_rds,
    dagster_fivetran_translator=CustomFivetranTranslator()
)

defs = dg.Definitions(
    assets=fivetran_specs
)
