import argparse
import yaml
import logging
from pyspark.sql import SparkSession
import importlib.resources as pkg_resources  #for reading resource files that are bundled inside Python packages.
from job_sources import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def load_config():
    with (
        pkg_resources.files(config)
                .joinpath("config.yaml")
                .open("r", encoding="utf-8") as f
        ):
        return yaml.safe_load(f)

def create_schema_and_grants(spark, config, env):
    base_catalog_name = config["catalog_base_name"]
    env_config = config["environments"][env]
    sp_application_id = env_config["sp_application_id"]
    team_name = env_config["team_name"]
    team_privileges = env_config["team_privileges"]
    human_users = env_config.get("human_users", [])

    for schema in config["schemas"]:
        schema_name = schema["name"]
        description = schema.get("description", "")
        full_schema = f"{base_catalog_name}_{env}.{schema_name}"

        logger.info(f"Creating schema: {full_schema}")
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {full_schema} COMMENT '{description}'")

        logger.info(f"Granting MANAGE to service principal {sp_application_id}")
        spark.sql(f"GRANT MANAGE ON SCHEMA {full_schema} TO `{sp_application_id}`")

        for privilege in team_privileges:
            logger.info(f"Granting {privilege} to team: {team_name}")
            spark.sql(f"GRANT {privilege} ON SCHEMA {full_schema} TO `{team_name}`")

        for user in human_users:
            logger.info(f"Granting SELECT to user: {user}")
            spark.sql(f"GRANT SELECT ON SCHEMA {full_schema} TO `{user}`")

def main():
    logger.info("Starting job to create schemas for customer-360 UC...")
    spark = SparkSession.builder.getOrCreate()

    logger.info("Loading configuration file...")
    config = load_config()

    # Get the env parameter from the wheel parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, help='Environment setting')
    args = parser.parse_args()
    env = args.env

    logger.info(f"\n=== Processing environment: {env} ===")
    create_schema_and_grants(spark, config, env)
    logger.info(f"\n=== Finished creating schemas for environment: {env} ===")


if __name__ == "__main__":
    main()
