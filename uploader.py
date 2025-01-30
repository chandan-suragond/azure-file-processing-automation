from azure.storage.blob import BlobServiceClient
import os
from config import *
from logger_config import logger


def upload_to_universal():
    """Upload all files from local directory to universal container"""
    
    logger.info("Entering upload_to_universal")

    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        
        container_client = blob_service_client.get_container_client(UNIVERSAL_CONTAINER)
        logger.info("container_client created")
        
        for root, dirs, files in os.walk(LOCAL_DIRECTORY):
            for file in files:
                logger.info(f"Picked up {file} from local directory")
                if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                    local_path = os.path.join(root, file)
                    blob_name = file  # Directly use filename in universal container
                    
                    logger.info(f"Beginning upload for {file}")
                    with open(local_path, "rb") as data:
                        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
                    logger.info(f"Uploaded {file} to universal container")
                    
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise

    finally:
        logger.info("Exiting upload_to_universal")