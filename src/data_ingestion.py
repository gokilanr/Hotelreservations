import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_function import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"DataIngestion started with {self.bucket_name} and file {self.file_name}")

    def download_csv_from_gcs(self):
        """
        Downloads a CSV file from a Google Cloud Storage bucket.
        """
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Downloaded {self.file_name} from bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading file from GCS: {e}")
            raise CustomException("Failed to download file from GCS", e)
    
    def split_data(self):
        """"
        splits the data into training and testing sets.
        """
        try:
            logger.info("Starting data splitting process")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Data split into train and test sets with ratio {self.train_test_ratio}")
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException("Failed to split data", e)
        
    def run(self):
        """
        Executes the data ingestion process: downloading and splitting the data.
        """
        try:
            logger.info("Running data ingestion process")
            self.download_csv_from_gcs()
            self.split_data()
            logger.info("Data ingestion process completed successfully")
        except Exception as e:
            logger.error(f"Error in data ingestion run method: {e}")
            raise CustomException("Data ingestion process failed", e)
        
        finally:
            logger.info("DataIngestion process finished")


if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()
