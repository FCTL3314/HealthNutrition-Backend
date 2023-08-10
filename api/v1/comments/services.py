from http import HTTPStatus

from rest_framework.response import Response


class CommentService:
    def __init__(self, serializer, request_data: dict, user):
        self._serializer = serializer
        self._request_data = request_data
        self._user = user

    def create(self):
        serializer = self._serializer(data=self._request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self._user)
        return Response(serializer.data, status=HTTPStatus.CREATED)
