import sys
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
from sensor.utils.main_utils import read_yaml_file

class DataValidation:
    
    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact, 
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = self._schema_config['columns']
            if len(dataframe.columns) == len(number_of_columns):
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)

    def drop_zero_std_columns(self, dataframe:pd.DataFrame):
        pass

    def is_numerical_column_exist(self, dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f'Missing numerical columns: {missing_numerical_columns}')
            return numerical_column_present

        except Exception as e:
            raise SensorException(e,sys)

    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise SensorException(e,sys)

    def detect_dataset_drift(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_validation(self) -> DataIngestionArtifact:
        try:
            error_message = ''
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f'{error_message} Train dataset does not contain all columns\n'
            status = self.validate_status(dataframe=test_dataframe)
            if not status:
                error_message = f'{error_message} Test dataset does not contain all columns\n'
            
            #Validate numerical columns
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f'{error_message} Train dataset does not contain all numerical columns\n'
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f'{error_message} Test dataset does not contain all numerical columns\n'

            if len(error_message) > 0:
                raise Exception(error_message)

            # lets check data drift
            
            

        except Exception as e:
            raise SensorException(e,sys)