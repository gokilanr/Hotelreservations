import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
import joblib
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_function import read_yaml, load_data
from scipy.stats import randint

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self,train_path,test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_slit_data(self):
        try:
            logger.info("loading data from {self.train_path} and {self.test_path}")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_Status'])
            y_train = train_df['booking_Status']

            X_test = test_df.drop(columns=['booking_Status'])
            y_test = test_df['booking_Status']

            logger.info("Data loaded and split into features and target")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error in load_and_split_data: {e}")
            raise CustomException("Data loading and splitting failed", e)
        
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Starting LightGBM model training with RandomizedSearchCV")
            lgbm = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])

            random_search = RandomizedSearchCV(
                estimator=lgbm,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )

            random_search.fit(X_train, y_train)

            logger.info(f"Best parameters found: {random_search.best_params_}")
            logger.info("LightGBM model training completed")

            logger.info("Hyperparameter tuning completed, best parameters obtained  and model trained")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters: {best_params}")
            
            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error in train_lgbm: {e}")
            raise CustomException("LightGBM model training failed", e)
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model performance on test data")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            logger.info(f"Model evaluation metrics - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }
        
        except Exception as e:
            logger.error(f"Error in evaluate_model: {e}")
            raise CustomException("Model evaluation failed", e)
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info(f"Saving model to {self.model_output_path}")
            joblib.dump(model, self.model_output_path)
            logger.info("Model saved successfully")

        except Exception as e:
            logger.error(f"Error in save_model: {e}")
            raise CustomException("Model saving failed", e)
    
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("starting our model training")
                logger.info("Logging model parameters and metrics to MLflow")
                
                logger.info("logging the training and testing dataset to mlflow")
                
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_slit_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging model into MLflow")

                mlflow.log_artifact(self.model_output_path)

                logger.info("loading parmas and metrics to mlflow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model training and logging to MLflow completed")

        except Exception as e:
            logger.error(f"Error in save_model: {e}")
            raise CustomException("Model saving failed", e)
        

if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_PATH, PROCESSED_TEST_PATH, MODEL_OUTPUT_PATH)
    trainer.run()
