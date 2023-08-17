from rest_framework.response import Response as DRFResponse


class APIResponse(DRFResponse):
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
        data_content = (data or self.build_error_data(detail, code, messages),)
        super().__init__(
            data_content, status, template_name, headers, exception, content_type
        )

    @staticmethod
    def build_error_data(
        detail: str,
        code: str,
        messages: dict[str] | list[str],
    ) -> dict[str] | None:
        data_content = {}
        if detail is not None:
            data_content["detail"] = detail
        if code is not None:
            data_content["code"] = code
        if messages is not None:
            data_content["messages"] = messages
        return data_content or None
