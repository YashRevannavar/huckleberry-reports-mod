from dotenv import load_dotenv
import os

load_dotenv()

BABY_NAME = os.getenv("BABY_NAME")
BABY_DOB = os.getenv("BABY_DOB")