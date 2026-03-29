from typing import List, Tuple
import pandas as pd
import os

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from .models import ActivityRecord
from .data_handler import DataHandler

logger = setup_logger(__name__)

class DataService:
    def __init__(self):
        self.handler = DataHandler()
        
    def fetch_parsed_data(self, file_path: str) -> Result[Tuple[List[ActivityRecord], pd.DataFrame]]:
        """
        Orchestrates fetch routing for parsed data.
        :param file_path: Path of CSV file
        :return: Result wrapping ActivityRecord List and DataFrame.
        """
        logger.info(f"Initiating data load for: {file_path}")
        if not os.path.exists(file_path):
            error_msg = f"File {file_path} does not exist."
            logger.error(error_msg)
            return Result(success=False, error=error_msg)
            
        return self.handler.load_data(file_path)
