from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from config import *
import time
from logger_config import logger


def process_file(blob_name):
    """Trigger pipeline and monitor execution"""

    logger.info("Entering process_file")

    try:
        # Determine pipeline from filename prefix
        prefix = blob_name.split('_')[0].lower()
        pipeline_name = next(
            (p for p in PIPELINE_NAMES if prefix in p.lower()),
            None
        )
        
        if not pipeline_name:
            raise ValueError(f"No pipeline found for prefix {prefix}")
            
        # Initialize ADF client
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, ADF_SUBSCRIPTION_ID)
        
        # Trigger pipeline
        pipeline_run = adf_client.pipelines.create_run(
            resource_group_name=ADF_RESOURCE_GROUP,
            factory_name=ADF_FACTORY_NAME,
            pipeline_name=pipeline_name,
            parameters={"filenamePrefix": prefix}
        )
        
        # Monitor pipeline
        start_time = time.time()
        while True:
            status = adf_client.pipeline_runs.get(
                resource_group_name=ADF_RESOURCE_GROUP,
                factory_name=ADF_FACTORY_NAME,
                run_id=pipeline_run.run_id
            ).status
            
            if status in ["Succeeded", "Failed", "Cancelled"]:
                logger.info(f"Pipeline {pipeline_name} completed with status: {status}")
                return status
                
            if time.time() - start_time > 1200:  # 20 minutes timeout
                raise TimeoutError("Pipeline execution timed out")
                
            time.sleep(30)
            
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
    
    finally: 
        logger.info("Exiting process_file")