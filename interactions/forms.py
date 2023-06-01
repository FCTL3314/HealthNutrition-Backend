from django import forms


class RecipeCommentForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Add a comment...',
        'type': 'text',
        'maxlength': '516',
    }))
