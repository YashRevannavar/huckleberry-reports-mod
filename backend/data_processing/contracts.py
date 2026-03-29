from abc import ABC, abstractmethod
from typing import Tuple, List
import pandas as pd
from .models import ActivityRecord
from backend.utilities.models import Result

class BaseDataLoader(ABC):
    
    @abstractmethod
    def load_data(self, file_path: str) -> Result[Tuple[List[ActivityRecord], pd.DataFrame]]:
        """
        Loads CSV data into typed ActivityRecord list and a Pandas DataFrame.
        :param file_path: Path to CSV data table.
        :return: Result wrapping output structures.
        """
        pass
