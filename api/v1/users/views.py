from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.users.serializers import (SendVerificationEmailSerializer,
                                      VerifyUserSerializer)
from api.v1.users.services import EmailVerificationSender, UserEmailVerifier
from users.models import EmailVerification, User


class EmailVerificationCreateAPIView(CreateAPIView):
    queryset = EmailVerification.objects.all()
    serializer_class = SendVerificationEmailSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data["email"]
        user = get_object_or_404(User, email__iexact=email)

        sender_service = EmailVerificationSender(user, request)
        return sender_service.send()


class VerifyUserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = VerifyUserSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = request.data["code"]
        email = request.data["email"]
        user = get_object_or_404(User, email__iexact=email)

        verifier_service = UserEmailVerifier(user, request, code)
        return verifier_service.verify()
