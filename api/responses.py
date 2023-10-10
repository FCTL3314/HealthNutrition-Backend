from typing import Iterable

from rest_framework.response import Response


class APIResponse(Response):
    """
    Extends the Response class from rest_framework by
    adding the following fields:

    detail - Detailed description of the response.
    code - The string code of the response.
    messages - The list of response messages.

    New fields are displayed only if the data argument has
    not been passed.
    """

    def __init__(
        self,
        data=None,
        detail=None,
        code=None,
        messages=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        super().__init__(
            data or self._build_error_data(detail, code, messages),
            status,
            template_name,
            headers,
            exception,
            content_type,
        )

    @staticmethod
    def _build_error_data(
        detail: str,
        code: str,
        messages: Iterable[str],
    ) -> dict[str, str]:
        data_content = {}
        if detail is not None:
            data_content["detail"] = detail
        if code is not None:
            data_content["code"] = code
        if messages is not None:
            data_content["messages"] = messages
        return data_content
