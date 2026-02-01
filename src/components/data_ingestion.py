import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import CustomException
from src.logger import loggerDI as logger
from src.data_access.proj1_data import Proj1Data

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def export_data_into_feature_store(self) -> DataFrame:
        """Exports data from MongoDB to feature store as a DataFrame"""
        try:
            logger.info("Exporting data from MongoDB to feature store")
            proj1_data = Proj1Data()
            df: DataFrame = proj1_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            logger.info(f"Data exported to feature store at {feature_store_file_path}")
            return df
        except Exception as e:
            logger.error("Error exporting data to feature store")
            raise CustomException(e, sys) from e
        
    def split_data_as_train_test(self,df:DataFrame) -> None:
        """Method to split data into train and test sets"""
        try:
            logger.info("Splitting data into train and test sets")
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            training_file_path = self.data_ingestion_config.training_file_path
            testing_file_path = self.data_ingestion_config.testing_file_path

            os.makedirs(os.path.dirname(training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(testing_file_path), exist_ok=True)

            train_set.to_csv(training_file_path, index=False, header=True)
            test_set.to_csv(testing_file_path, index=False, header=True)

            logger.info(f"Training and testing data saved at {training_file_path} and {testing_file_path}")
        except Exception as e:
            logger.error("Error splitting data into train and test sets")
            raise CustomException(e, sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """Mehtod to initiate data ingestion"""
        try:
            logger.info("Starting data ingestion process")
            df: DataFrame = self.export_data_into_feature_store()
            self.split_data_as_train_test(df=df)

            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
            )

            logger.info(f"Data ingestion completed with artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            logger.error("Error in data ingestion process")
            raise CustomException(e, sys) from e