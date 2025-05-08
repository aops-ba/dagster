import dagster as dg
from dagster_dbt import (
    DbtCliResource,
    DbtProject,
    dbt_assets,
    DagsterDbtTranslator
)
from pathlib import Path

DBT_PATH = Path("../aops-analytics").resolve()

my_project = DbtProject(
    project_dir=DBT_PATH
)

dbt_resource = DbtCliResource(project_dir=my_project)

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props):
        return "dbt"

@dbt_assets(
    manifest=my_project.manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def my_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

defs = dg.Definitions(
    assets=[my_dbt_assets]
)
