from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.models import User


class EmailVerificationMixin(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        email = self.request.data.get("email")
        return get_object_or_404(User, email__iexact=email)
