import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

MONGO_URI = os.environ.get("MONGO_URI")

CACHE_TYPE = os.environ.get("CACHE_TYPE")

CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT")