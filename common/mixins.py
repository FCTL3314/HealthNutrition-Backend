class RequestDataValidationMixin:
    """
    Validates the request data using a serializer.
    """

    def validate_request_data(self, raise_exception=True):
        serializer = self.get_serializer(data=self.request.data)
        return serializer.is_valid(raise_exception=raise_exception)
