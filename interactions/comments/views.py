from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from interactions.comments.forms import ProductCommentForm, StoreCommentForm
from interactions.comments.models import ProductComment, StoreComment
from products.models import Product
from stores.models import Store
from utils.urls import get_referer_or_default


class BaseCommentFormView(LoginRequiredMixin, FormView):
    comment_model: Model = None
    related_model: Model = None
    identifier_field: str = "slug"

    def form_valid(self, form):
        text = form.cleaned_data.get("text")
        self._create_comment(text)
        return super().form_valid(form)

    def _create_comment(self, text: str):
        comment_data = {
            "text": text,
            "author": self.request.user,
            self.related_model._meta.model_name: self._get_related_object(),
            **self.get_comment_creation_extra_kwargs(),
        }
        self.comment_model.objects.create(**comment_data)

    @staticmethod
    def get_comment_creation_extra_kwargs() -> dict:
        return {}

    def _get_identifier(self) -> Optional:
        return self.kwargs.get(self.identifier_field)

    def _get_related_object(self):
        kwargs = {self.identifier_field: self._get_identifier()}
        return get_object_or_404(self.related_model, **kwargs)

    def get_success_url(self):
        return get_referer_or_default(self.request)


class ProductCommentView(BaseCommentFormView):
    comment_model = ProductComment
    related_model = Product
    form_class = ProductCommentForm


class StoreCommentView(BaseCommentFormView):
    comment_model = StoreComment
    related_model = Store
    form_class = StoreCommentForm
