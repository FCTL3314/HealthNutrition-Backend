from django import forms

from interactions.comments.models import ProductComment, StoreComment


class BaseCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Add a comment...",
                "type": "text",
                "maxlength": "516",
            }
        )
    )


class ProductCommentForm(BaseCommentForm):
    class Meta:
        fields = ("text",)
        model = ProductComment


class StoreCommentForm(BaseCommentForm):
    class Meta:
        fields = ("text",)
        model = StoreComment
