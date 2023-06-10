from django.conf import settings


def common_detail_view_tests(response, obj, comments=None):
    obj.refresh_from_db()
    assert response.context_data['object'] == obj
    assert obj.views == 1
    if comments is not None:
        assert len(response.context_data['comments']) == len(comments[:settings.COMMENTS_PAGINATE_BY])
