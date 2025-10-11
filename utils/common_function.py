import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml


logger = get_logger(__name__)

def read_yaml(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (str): The path to the YAML file. 

    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {file_path} read successfully.")
            return config
        
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException("Failed to read yaml file", e)
    
def load_data(file_path):
    try:
        logger.info("loading data")
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise CustomException("Failed to load data", e)