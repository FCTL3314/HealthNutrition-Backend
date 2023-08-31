import pytest
from django.db.models import Model
from mixer.backend.django import mixer

from api.v1.products.models import Product, ProductType
from api.v1.search.serializers import SearchSerializer
from api.v1.search.services import (
    BaseSearchService,
    ProductSearchService,
    ProductTypeSearchService,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model, service, search_field",
    [
        (ProductType, ProductTypeSearchService, "name"),
        (ProductType, ProductTypeSearchService, "description"),
        (Product, ProductSearchService, "name"),
        (Product, ProductSearchService, "card_description"),
    ],
)
def test_search_service(
    model: type[Model],
    service: type[BaseSearchService],
    search_field: str,
):
    model_object = mixer.blend(model)
    search_attr = getattr(model_object, search_field)
    service = service(
        SearchSerializer,
        {"query": search_attr},
    )
    expected_queryset = model.objects.search(search_attr)
    actual_queryset = service.get_searched_queryset()
    assert list(expected_queryset) == list(actual_queryset)


if __name__ == "__main__":
    pytest.main()
