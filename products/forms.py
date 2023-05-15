from django import forms


class SearchForm(forms.Form):
    choices = [
        ('product', 'Product'),
        ('category', 'Category'),
    ]

    search_query = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'search',
                'placeholder': 'Enter the name of the product or category you are looking for...',
            }
        )
    )
    search_type = forms.ChoiceField(
        choices=choices,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
