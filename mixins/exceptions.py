from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

class InvalidRequestException(APIException):
    status_code = 400  # HTTP status code for internal server error
    default_detail = "Something Went Wrong"
    default_code = "error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        self.detail = {"error": str(detail)}
        super().__init__(detail=detail, code=code)

# Custom exception handler to return the new format
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    # If an APIException, modify the response structure
    if response is not None and isinstance(exc, APIException):
        response.data = {"error": response.data.get("detail", "Something Went Wrong")}
    
    return response