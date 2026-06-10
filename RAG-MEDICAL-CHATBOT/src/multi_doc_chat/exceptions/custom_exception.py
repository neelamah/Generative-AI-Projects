#To show custom errors.
#if there is built-in error like divide by zero, which is not easily understand. so, file not found, etc. for this we can show custom error.

import sys

# This function is used to get detailed error message from the exception object.
#here we are getting what is ther built in error and where it is coming from.
class CustomException(Exception):
    def __init__(self, message, error_detail: Exception=None):
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    #  _, _, exc_tb contain the exception type, value, and traceback information.
    #we filterout filename and line number from the traceback information to provide a more detailed error message.
    @staticmethod
    def get_detailed_error_message(message: str, error_detail):
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return (
                f"{ message} | " # message is the custom message we want to show when the error occurs.
                f"Error: {error_detail} | " # error_detail is the built-in error message that we get from the exception object.
                f"File: {file_name} | " # file_name is the name of the file where the error occurred.
                f"Line: {line_number}" # line_number is the line number where the error occurred.
            )
        
        
    def __str__(self):
        return self.error_message