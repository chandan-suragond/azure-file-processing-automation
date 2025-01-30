from azure.storage.blob import BlobServiceClient
from config import *
from logger_config import logger


def copy_to_source(blob_name):
    """Copy file from universal container to source container with folder structure"""

    logger.info("Entering copy_to_source")

    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        
        # Extract folder structure from filename (cocoblu_rebini.csv -> cocoblu/rebini/)
        parts = blob_name.split('_')
        if len(parts) < 2:
            raise ValueError("Invalid filename format")
            
        folder_path = f"{parts[0]}/{parts[1].split('.')[0]}"
        target_blob_name = f"{folder_path}/{blob_name}"
        
        # Get blob clients
        source_client = blob_service_client.get_blob_client(
            container=UNIVERSAL_CONTAINER,
            blob=blob_name
        )
        
        dest_client = blob_service_client.get_blob_client(
            container=SOURCE_CONTAINER,
            blob=target_blob_name
        )
        
        # Start copy operation
        dest_client.start_copy_from_url(source_client.url)
        logger.info(f"Copied {blob_name} to source container")
        
        return target_blob_name
        
    except Exception as e:
        logger.error(f"Copy failed: {e}")
        raise
    
    finally:
        logger.info("Exiting copy_to_source")