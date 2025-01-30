from azure.storage.blob import BlobServiceClient
from config import *
from logger_config import logger


def archive_file(blob_name, status):
    """Move file to success/failure archive"""

    logger.info("Entering archive_file")

    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        
        # Construct destination path
        archive_folder = "success_archival" if status == "Succeeded" else "failure_archival"
        dest_blob_name = f"{archive_folder}/{blob_name}"
        
        # Get blob clients
        source_client = blob_service_client.get_blob_client(
            container=UNIVERSAL_CONTAINER,
            blob=blob_name
        )
        
        dest_client = blob_service_client.get_blob_client(
            container=DESTINATION_CONTAINER,
            blob=dest_blob_name
        )
        
        # Copy and delete original
        dest_client.start_copy_from_url(source_client.url)
        source_client.delete_blob()
        logger.info(f"Moved {blob_name} to {archive_folder}")
        
    except Exception as e:
        logger.error(f"Archiving failed: {e}")
        raise

    finally:
        logger.info("Exiting archive_file")