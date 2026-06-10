from src.multi_doc_chat.exceptions.custom_exception import CustomException

try:
    x = 1 / 0
except Exception as e:
     raise CustomException("An error occurred while dividing by zero.", e)