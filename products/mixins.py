from django.views.generic.edit import FormMixin


class SearchFormMixin(FormMixin):
    """
    A mixin for adding search query to the form initial
    and context data.
    """

    search_query_field = "search_query"
    search_type_field = "search_type"

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get(self.search_query_field, "")
        self.search_type = self.request.GET.get(self.search_type_field)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial[self.search_query_field] = self.search_query
        initial[self.search_type_field] = self.search_type
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.search_query_field] = self.search_query
        context[self.search_type_field] = self.search_type
        return context
