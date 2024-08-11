from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.views import exception_handler

from django.http.response import Http404


class ErrorResponse(Response):
    def __init__(self, message, code, status):
        data = {
            "message": message,
            "code": code,
        }
        super().__init__(data=data, status=status)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is None:
        return response
    if isinstance(exc, Http404):
        response.data["detail"].code = "OBJECT_NOT_FOUND"

    if isinstance(exc, ValidationError):
        message = {}
        if isinstance(exc.detail, ReturnList):
            message.update({k: v for inner_dict in exc.detail for k, v in inner_dict.items()})
        else:
            message.update(exc.detail)
        return ErrorResponse(message, "BAD_REQUEST_STRUCTURE", response.status_code)

    if "detail" in response.data:
        message = str(response.data["detail"])
        code = response.data["detail"].code
        return ErrorResponse(message, code, response.status_code)

    return response


class ResponseJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
            "data": data,
            "error": {},
        }
        if renderer_context["response"].status_code == 204:
            response = data
        elif not str(status_code).startswith("2"):
            response["data"] = {}
            response["error"] = data

        return super(ResponseJsonRenderer, self).render(response, accepted_media_type, renderer_context)
