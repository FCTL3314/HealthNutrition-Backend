from django.utils.text import slugify


class SlugifyMixin:
    def change_slug(self, field_to_slugify: str, commit=True) -> None:
        string_to_slugify = getattr(self, field_to_slugify)
        self.slug = slugify(string_to_slugify)
        if commit:
            self.save(update_fields=("slug",))


class IncrementMixin:
    def increase(self, field: str, value: int = 1, commit=True) -> None:
        setattr(self, field, getattr(self, field) + value)
        if commit:
            self.save(update_fields=(field,))
