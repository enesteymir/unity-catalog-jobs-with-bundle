
CREATE SCHEMA IF NOT EXISTS customer_360_catalog_test.archive;
GRANT MANAGE ON SCHEMA customer_360_catalog_test.archive TO `883dbeee-bcb7-4678-97da-34442708fea5`; -- application id of "app_customer-360-unity-catalog+test+sp@zalando.de"
GRANT MANAGE ON SCHEMA customer_360_catalog_test.archive TO `acc-team-tracking-t-rex-test`;

-- customer_curated_data.customer_behaviour_source -- Dropping first, not possible to "create or replace" EXTERNAL tables
DROP TABLE IF EXISTS customer_360_catalog_test.archive.message_psd;
CREATE EXTERNAL TABLE customer_360_catalog_test.archive.message_psd
LOCATION "s3://customer-360-data-platform-test/archive/message_psd";