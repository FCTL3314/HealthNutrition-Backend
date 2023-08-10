from http import HTTPStatus

from rest_framework.response import Response


class CommentService:
    def __init__(self, serializer, request):
        self.serializer = serializer
        self.request = request

    def create(self):
        serializer = self.serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=HTTPStatus.CREATED)
