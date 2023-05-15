from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.base import ContextMixin, View


class TitleMixin(ContextMixin):
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'StoreTracker | {self.title}' if self.title else 'StoreTracker'
        return context


class LogoutRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
