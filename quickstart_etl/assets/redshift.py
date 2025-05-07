from dagster import Definitions, asset
from dagster_aws.redshift import RedshiftClientResource

@asset
def example_redshift_asset(context, redshift: RedshiftClientResource):
    result = redshift.get_client().execute_query(
        "SELECT * FROM dbt_flevine.email_categories_sendgrid LIMIT 10",
        fetch_results=True
    )
    context.log.info(f"Query result: {result}")
    # write the result to a file
    with open("data/example_redshift_asset.txt", "w") as f:
        f.write(str(result))


defs = Definitions(
    assets=[example_redshift_asset]
)
