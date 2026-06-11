#os - is a built-in module in Python that provides a way to interact with the operating system. 
# It allows you to perform various tasks such as reading and writing files, managing directories, and accessing environment variables.
#dotenv - is a third-party library that allows you to load environment variables from a .env file into your Python application.
#getenv - is a function provided by the os module that retrieves the value of an environment variable. It takes the name of the variable as an argument and returns its value as a string. If the variable does not exist, it returns None or a default value if specified.


#config.py -># app settings
#pyproject.toml- > # project metadata + dependencies
#.env -> # environment variables (API keys, database credentials, etc.)

import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env file
#to  pass the API key securely without hardcoding it in the codebase, we can use environment variables. 
# This way, we can keep sensitive information like API keys out of the code and easily manage them across
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"