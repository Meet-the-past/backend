
from datetime import datetime

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response

from .custom_exceptions import *
# from .settings import logger
from .exception_codes import STATUS_RSP_INTERNAL_ERROR

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        if isinstance(exc, ValidationError):
            code = response.status_code
            msg = ValidationError.msg
            response.status_code = 401
            

        else:
            code = response.status_code
            msg = "unknown error"

        response.status_code = code
        #response.data['code'] = code
        response.data['message'] = msg
        #response.data['data'] = None

        response.data.pop('detail', None)

        return response
    else:
        STATUS_RSP_INTERNAL_ERROR['message'] = STATUS_RSP_INTERNAL_ERROR.pop('default_message', None)
        STATUS_RSP_INTERNAL_ERROR['data'] = None
        STATUS_RSP_INTERNAL_ERROR.pop('lang_message', None)
        return Response(STATUS_RSP_INTERNAL_ERROR, status=500)
    
            

#         else:
#             code = response.status_code
#             msg = "unknown error"

    return response
