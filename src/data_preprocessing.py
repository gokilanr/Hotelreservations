import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_function import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self, train_path,test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir, exist_ok=True)

    
    def preprocess_data(self):
        try:
            logger.info("Starting data preprocessing")
            logger.info("dropping unnecessary columns")

            df.drop(columns=['Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            caset_cols = self.config['categorical_columns']
            num_cols = self.config['numerical_columns']

            logger.info("Applying label encoding to categorical columns")
            le = LabelEncoder()

            mapping_dict = {}

            for col in caset_cols:
                df[col] = le.fit_transform(df[col])
                mapping_dict[col] = dict(zip(le.classes_, le.transform(le.classes_)))
                logger.info(f"Label encoding applied to column: {col}")
            
            logger.info("Mapping dictionary for label encoding created")

            for col,map_dict in mapping_dict.items():
                logger.info(f"Mapping for column {col}: {map_dict}")

            logger.info("Doing skewness handling")

            skew_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())
            
            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])
                
            return df
        
        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise CustomException("Data preprocessing failed", e)
        