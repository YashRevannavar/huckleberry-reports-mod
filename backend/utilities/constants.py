import os
from dotenv import load_dotenv

load_dotenv()

BABY_NAME = os.getenv("BABY_NAME", "Baby")
BABY_DOB = os.getenv("BABY_DOB", "01-01-2024")
