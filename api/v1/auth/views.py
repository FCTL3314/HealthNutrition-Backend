from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.auth.serializers import UIDAndTokenSerializer


class CheckUIDAndToken(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        serializer = UIDAndTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.NOT_FOUND, data=serializer.errors)
