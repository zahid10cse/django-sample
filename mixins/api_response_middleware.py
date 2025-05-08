from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework.views import exception_handler
from django.db import IntegrityError
import traceback
from rest_framework.response import Response


class APIResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Implementation goes here
        # Check if 'Content-Type' header exists in the response
        if request.path.startswith("/swagger") or request.path.startswith("/docs"):
            return response  # skip wrapping

        if isinstance(response, Response) and "success" in response.data:
            return response
        content_type = response.headers.get('Content-Type', '')

        # Skip custom processing for HTML responses (e.g., Swagger UI)
        if 'text/html' in content_type:
            return response

        # Check if it's an error (e.g., 4xx or 5xx)
        data = {}
        errors = {}
        if 200 <= response.status_code < 300:
            success = True
            message = "Request Successful"
            data = response.data if hasattr(response, 'data') else {}
        else:
            success = False
            message = response.reason_phrase or "An error occurred"

            errors = response.data if hasattr(response, 'data') else {}

        # Build the custom response structure
        # custom_response = {
        #     'status': ,
        #     'message': message,
        #     'data': data
        # }
        custom_response ={
            "success": success,
            "message": message,
            "response": {
                "data": data ,
            },
            "errors": errors or []
        }

        # Return the custom formatted response as a JsonResponse
        return JsonResponse(custom_response, status=response.status_code)
    
    def process_exception(self, request, exception):
        # Implementation goes here
        # Use DRF's exception handler first
        response = exception_handler(exception, None)
        print(exception)
        if response is not None:
            return self.process_response(request, response)

        # Handle IntegrityError and other exceptions explicitly
        if isinstance(exception, IntegrityError):
            return JsonResponse({
                'success': False,
                'message': str(exception),
                'response':{
                    "data": {}
                },
                "errors":str(exception)
            }, status=400)
        

        # For non-DRF handled exceptions
        return JsonResponse({
            'success': False,
                'message': str(exception),
                'response':{
                    "data": {}
                },
                "errors":str(exception)
        }, status=500)

