from dagster import EnvVar
from dagster_aws.redshift import RedshiftClientResource
from dagster_airbyte import AirbyteResource

redshift = RedshiftClientResource(
    host=EnvVar("REDSHIFT_HOST"),
    port=EnvVar.int("REDSHIFT_PORT"),
    user=EnvVar("REDSHIFT_USER"),
    password=EnvVar("REDSHIFT_PASSWORD"),
    database=EnvVar("REDSHIFT_DATABASE"),
)

airbyte = AirbyteResource(
    host=EnvVar("AIRBYTE_HOST"),
    port=EnvVar("AIRBYTE_PORT"),
    username=EnvVar("AIRBYTE_USER"),
    password=EnvVar("AIRBYTE_PASSWORD"),
    use_https=True
)
