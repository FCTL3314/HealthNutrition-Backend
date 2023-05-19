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
        ('product', 'Product'),
        ('product_type', 'Category'),
    ]

    search_type = forms.ChoiceField(
        choices=choices,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )

    def clean_search_type(self):
        if self.search_type not in ('product', 'product_type'):
            return forms.ValidationError('Invalid search type')
        return self.search_type

    def __init__(self, search_query, search_type, *args, **kwargs):
        super().__init__()
        self.initial['search_query'] = search_query
        self.initial['search_type'] = search_type
