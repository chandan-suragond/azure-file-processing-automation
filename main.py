from logger_config import logger
from azure.storage.blob import BlobServiceClient
from uploader import upload_to_universal
from copier import copy_to_source
from processor import process_file
from mover import archive_file
from config import *
import time


def main():
    try:
        # Step 1: Upload all local files to universal container
        upload_to_universal()
        
        # Step 2: Process files sequentially
        blob_service_client = BlobServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=STORAGE_ACCOUNT_KEY
        )
        
        container_client = blob_service_client.get_container_client(UNIVERSAL_CONTAINER)
        
        for blob in container_client.list_blobs():
            try:
                logger.info(f"Processing {blob.name}")
                
                # Step 2a: Copy to source container
                source_blob_path = copy_to_source(blob.name)
                
                # Step 2b: Process file
                status = process_file(blob.name)
                
                # Step 2c: Archive in destination container
                archive_file(blob.name, status)
                
                logger.info(f"Completed processing {blob.name}")
                
            except Exception as e:
                logger.error(f"Failed to process {blob.name}: {e}")
                # Move to failure archive on any error
                archive_file(blob.name, "Failed")
                continue
                
    except Exception as e:
        logger.error(f"Main process failed: {e}")
        raise

if __name__ == "__main__":
    main()