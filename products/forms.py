from django import forms


class SearchForm(forms.Form):
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

    choices = [
        ('product_type', 'Category'),
        ('product', 'Product'),
    ]

    search_type = forms.ChoiceField(
        choices=choices,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )

    def __init__(self, search_query=None, search_type=None, *args, **kwargs):
        super().__init__()
        self.initial['search_query'] = search_query
        self.initial['search_type'] = search_type
