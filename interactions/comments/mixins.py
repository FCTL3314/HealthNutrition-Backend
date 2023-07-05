from abc import ABC, abstractmethod
from typing import Optional

from django.db.models import Model
from django.shortcuts import get_object_or_404

from users.models import User


class CommentCreateMixin(ABC):
    comment_model: Model = None
    related_model: Model = None
    identifier_field: str = "slug"
    identifier_kwarg: str = identifier_field

    def create_comment(self, text: str, author: User) -> comment_model:
        kwargs = {
            "text": text,
            "author": author,
            self.related_model._meta.model_name: self._get_related_object(),
            **self.get_comment_creation_extra_kwargs(),
        }
        return self.comment_model.objects.create(**kwargs)

    @staticmethod
    def get_comment_creation_extra_kwargs() -> dict:
        return {}

    @abstractmethod
    def get_identifier(self) -> Optional:
        pass

    def _get_related_object(self) -> related_model:
        kwargs = {self.identifier_field: self.get_identifier()}
        return get_object_or_404(self.related_model, **kwargs)
