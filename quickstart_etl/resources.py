from dagster_aws.redshift import RedshiftClientResource
from dagster import Definitions, asset, EnvVar

redshift = RedshiftClientResource(
    host=EnvVar("REDSHIFT_HOST"),
    port=EnvVar.int("REDSHIFT_PORT"),
    user=EnvVar("REDSHIFT_USER"),
    password=EnvVar("REDSHIFT_PASSWORD"),
    database=EnvVar("REDSHIFT_DATABASE"),
)
