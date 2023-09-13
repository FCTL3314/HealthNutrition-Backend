from drf_spectacular.utils import extend_schema, extend_schema_view


def product_comment_view_set_docs():
    return extend_schema_view(
        create=extend_schema(
            summary="Adds a comment to a specific product.",
        )
    )


def store_comment_view_set_docs():
    return extend_schema_view(
        create=extend_schema(
            summary="Adds a comment to a specific store.",
        )
    )
