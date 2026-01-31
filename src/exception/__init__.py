import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """Extract detailed error information including filename, line number, and error message."""
    
    # Extract the traceback information (exception information)
    _, _, exc_tb = error_detail.exc_info()

    # Get the filename where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Create a formatted error message string with filename, line number, and error message
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in file: [{file_name}] at line: [{line_number}] with message: [{str(error)}]"

    # log the error message
    logging.error(error_message)

    return error_message

class CustomException(Exception):
    """Custom exception class for handling errors"""
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initialize the CustomException with a detailed error message.

        :param error_message: The error message to be included in the exception.
        :param error_detail: The sys module to extract exception details.
        """
        # Call the base class constructor with the parameters it needs
        super().__init__(error_message)

        # Format the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(
            error_message, error_detail
        )


    def __str__(self)-> str:
        """Return the detailed error message when the exception is converted to a string."""
        return self.error_message