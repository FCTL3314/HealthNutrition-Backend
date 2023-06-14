from django.core.exceptions import PermissionDenied


class ProfileMixin:
    template_name = "users/profile/profile.html"

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        if self.request.user.is_anonymous or self.request.user.slug != slug:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
