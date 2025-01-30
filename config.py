# config.py

# Azure Storage Configuration
STORAGE_ACCOUNT_NAME = "STORAGE_ACCOUNT_NAME"
STORAGE_ACCOUNT_KEY = "STORAGE_ACCOUNT_KEY"
UNIVERSAL_CONTAINER = "universal-container"
SOURCE_CONTAINER = "cont-input"
DESTINATION_CONTAINER = "cont-output"

# ADF Configuration
ADF_SUBSCRIPTION_ID = "ADF_SUBSCRIPTION_ID"
ADF_RESOURCE_GROUP = "ADF_RESOURCE_GROUP"
ADF_FACTORY_NAME = "ADF_FACTORY_NAME"
PIPELINE_NAMES = [
      "test_pipeline_cocoblu", 
      "test_pipeline_retailez"
]

# Local Paths
LOCAL_DIRECTORY = "C:/Users/ChandanSuragond/Downloads/local_folder/"
SUPPORTED_EXTENSIONS = [".xls", ".xlsx", ".xlsb", ".csv"]