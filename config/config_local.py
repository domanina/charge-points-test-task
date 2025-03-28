import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SRVC_URL_API = os.environ.get("SRVC_URL_API", "http://localhost:3001/")
SRVC_URL_UI = os.environ.get("SRVC_URL_UI", "http://localhost:3000/")
RUN_BROWSER = os.environ.get("RUN_BROWSER", "webkit")
