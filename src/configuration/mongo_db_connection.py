"""This module handles the MongoDB connection setup."""

import os
import sys
import pymongo
import certifi

from src.exception import CustomException
from src.logger import loggerConfig as logger
from src.constants import MONGODB_URL_KEY, DATABASE_NAME

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    ----------
    client : MongoClient
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MongoDBClient connects to.

    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.
    """

    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes the MongoDB connection using the given database name.

        Parameters:
        ----------
        database_name : str, optional
            The name of the database to connect to. Default is DATABASE_NAME from constants.
        """
        try:
            if MongoDBClient.client is None:
                mongodb_url = MONGODB_URL_KEY
                if mongodb_url is None:
                    raise Exception("MongoDB URL is not provided.")
                
                MongoDBClient.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)


            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logger.info(f"Successfully connected to MongoDB database: {database_name}")
        
        except Exception as e:
            logger.error(f"Error while connecting to MongoDB: {e}")
            raise CustomException(e, sys) from e
        
if __name__ == "__main__":
    mongo_client = MongoDBClient()
    print(mongo_client.database)