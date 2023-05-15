from django.views.generic.base import ContextMixin


class TitleMixin(ContextMixin):
    title: str = 'Untitled'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
