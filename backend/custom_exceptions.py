from rest_framework.exceptions import APIException


class ValidationError(APIException):
    status_code = 401
    msg="만료되었거나 유효하지 않은 토큰입니다."


    
