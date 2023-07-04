from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.users.serializers import EmailVerificationSerializer
from users.models import EmailVerification, User
from api.v1.users.services import EmailVerificationService


class EmailVerificationCreateAPIView(CreateAPIView):
    queryset = EmailVerification.objects.all()
    serializer_class = EmailVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = get_object_or_404(User, email__iexact=email)

        verification_service = EmailVerificationService(user, request)
        return verification_service.send_verification(
            serializer_class=self.serializer_class
        )


class VerifyUserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        code = request.data.get('code')
        email = request.data.get('email')
        user = get_object_or_404(User, email__iexact=email)

        verification_service = EmailVerificationService(user, request)
        return verification_service.verify_user(code=code)
