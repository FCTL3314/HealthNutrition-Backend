import pytest
from django.urls import reverse
from django.utils.text import slugify
from mixer.backend.django import mixer


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, slug_related_field',
    [
        ('stores.Store', 'name'),
        ('products.Product', 'name'),
        ('users.User', 'username'),
    ],
)
def test_model_slug_update(model, slug_related_field):
    """
    Checks that the object's slug is created on object creation
    and updated on update.
    """
    string_to_slugify = 'Test Object'
    test_object = mixer.blend(model, **{slug_related_field: string_to_slugify})
    assert test_object.slug == slugify(string_to_slugify)

    updated_string_to_slugify = 'Updated Test Object'
    setattr(test_object, slug_related_field, updated_string_to_slugify)
    test_object.save()
    assert test_object.slug == slugify(updated_string_to_slugify)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, related_object_kwarg, comment_model',
    [
        ('stores.Store', 'store', 'interactions.StoreComment'),
        ('products.Product', 'product', 'interactions.ProductComment'),
    ],
)
def test_model_get_comments(model, related_object_kwarg, comment_model):
    test_object = mixer.blend(model)

    objects_number = 5
    mixer.cycle(objects_number).blend(comment_model, **{related_object_kwarg: test_object})
    comments = test_object.get_comments()
    assert len(comments) == objects_number


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, url_pattern, identifier_field',
    [
        ('stores.Store', 'stores:store-detail', 'slug'),
        ('products.Product', 'products:product-detail', 'slug'),
    ],
)
def test_model_get_absolute_url(model, url_pattern, identifier_field):
    test_object = mixer.blend(model)

    expected_url = reverse(url_pattern, args=(getattr(test_object, identifier_field),))
    actual_url = test_object.get_absolute_url()

    assert expected_url == actual_url


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, increment_field',
    [
        ('stores.Store', 'views'),
        ('products.ProductType', 'views'),
        ('products.Product', 'views'),
    ],
)
def test_model_increment(model, increment_field):
    test_object = mixer.blend(model)

    test_object.increase(increment_field, 1)

    assert getattr(test_object, increment_field) == 1


if __name__ == '__main__':
    pytest.main()
