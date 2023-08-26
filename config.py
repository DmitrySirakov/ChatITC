"""
Configuration module.
Loads environment variables from .env file and sets them for further usage.
"""

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ('TOKEN')
OPENAI_API_KEY = os.environ('OPENAI_API_KEY')
