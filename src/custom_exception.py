import traceback
import sys

class CustomException(Exception):

    def __init__(self, erro_message,error_detail:sys):
        super().__init__(erro_message)
        self.error_message = self.get_detailed_error_message(erro_message, error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail:sys):

        _, _, exc_tb = error_detail.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename

        detailed_message = f"Error occurred in script: {file_name} at line number: {line_number} with message: {error_message}"
        return detailed_message
    
    def __str__(self):
        return self.error_message
    