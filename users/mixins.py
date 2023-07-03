class ProfileMixin:
    template_name = "users/profile/settings.html"

    def get_object(self, *args, **kwargs):
        return self.request.user
