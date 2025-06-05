DROP TABLE IF EXISTS customer_360_catalog_test.archive.message_psd;
CREATE EXTERNAL TABLE customer_360_catalog_test.archive.message_psd
LOCATION "s3://customer-360-data-platform-test/archive/message_psd";
