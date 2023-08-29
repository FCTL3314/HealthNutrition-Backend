from typing import Any

from rest_framework.response import Response


class APIResponse(Response):
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
            data or self.build_error_data(detail, code, messages),
            status,
            template_name,
            headers,
            exception,
            content_type,
        )

    @staticmethod
    def build_error_data(
        detail: str,
        code: str,
        messages: list[str] | tuple[str] | dict[str, Any],
    ) -> dict[str, Any]:
        data_content = {}
        if detail is not None:
            data_content["detail"] = detail
        if code is not None:
            data_content["code"] = code
        if messages is not None:
            data_content["messages"] = messages
        return data_content
