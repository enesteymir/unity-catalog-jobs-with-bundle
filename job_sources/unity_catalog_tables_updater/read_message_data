from pyspark.sql import SparkSession
from databricks.sdk import WorkspaceClient
import logging

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    databricks_workspace_client = WorkspaceClient()
    databricks_workspace_client.dbutils.widgets.text("env", "test")
    # Get from the environment
    env = databricks_workspace_client.dbutils.widgets.get("env")
    logger.info(f"Retrieved widget value for env: {env}")
    if env != 'test':
        return

    try:
        spark = SparkSession.builder.getOrCreate()
        spark.catalog.setCurrentCatalog(f"customer_360_catalog_{env}")
        spark.catalog.setCurrentDatabase("archive")
        message_psd_df = spark.sql(f"select * from message_psd")
        logger.info(f"Successfully read table, number of rows: {message_psd_df.count()}")
    except Exception as e:
        logger.warning(f"Something went wrong {e}")


if __name__ == "__main__":
    main()

