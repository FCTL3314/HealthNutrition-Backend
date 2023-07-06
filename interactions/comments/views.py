from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from interactions.comments.forms import ProductCommentForm, StoreCommentForm
from interactions.comments.mixins import CommentCreateMixin
from interactions.comments.models import ProductComment, StoreComment
from products.models import Product
from stores.models import Store
from utils.urls import get_referer_or_default


class BaseCommentCreateFormView(LoginRequiredMixin, CommentCreateMixin, FormView):

    def form_valid(self, form):
        text = form.cleaned_data.get("text")
        self.create_comment(text=text, author=self.request.user)
        return super().form_valid(form)

    def get_identifier(self):
        return self.kwargs.get(self.identifier_field)

    def get_success_url(self):
        return get_referer_or_default(self.request)


class StoreCommentCreateView(BaseCommentCreateFormView):
    comment_model = StoreComment
    related_model = Store
    form_class = StoreCommentForm


class ProductCommentCreateView(BaseCommentCreateFormView):
    comment_model = ProductComment
    related_model = Product
    form_class = ProductCommentForm
