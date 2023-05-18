from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.base import ContextMixin, View


class TitleMixin(ContextMixin):
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        context['title'] = f'StoreTracker | {title}' if title else 'StoreTracker'
        return context


class LogoutRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
