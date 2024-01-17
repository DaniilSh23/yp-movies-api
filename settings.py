import os

from dotenv import load_dotenv

load_dotenv()

BASE_ELASTIC_URL = os.environ.get("BASE_ELASTIC_URL")
ELASTIC_PASSWD = os.environ.get("ELASTIC_PASSWD")
