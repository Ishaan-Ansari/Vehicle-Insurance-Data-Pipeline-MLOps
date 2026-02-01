from src.logger import loggerdemo as logger
from src.exception import CustomException
import sys

try:
    a = 1 + '1'  
except Exception as e:
    logger.error("An error occurred in demo script")
    raise CustomException(e, sys) from e