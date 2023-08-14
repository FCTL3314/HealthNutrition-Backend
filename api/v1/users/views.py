from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from api.v1.users.dependencies import EVSenderContainer
from api.v1.users.models import EmailVerification
from api.v1.users.serializers import EmailVerificationSerializer
from api.v1.users.services import EmailVerificationDTO, UserDTO
from api.v1.users.services.email_verification.email_verification_sender import (
    EVSendingResponse,
    EVSendingStatus,
)
from api.v1.users.services.email_verification.user_email_verifier import (
    UserEmailVerifierService,
)


class EmailVerificationCreateAPIView(CreateAPIView):
    serializer_class = EmailVerificationSerializer

    def create(self, request, *args, **kwargs):
        response: EVSendingResponse = (
            EVSenderContainer.email_verification_sender.execute(
                UserDTO.to_dto(request.user),
                EmailVerificationDTO.to_dto(
                    EmailVerification.objects.last_sent(request.user.id),
                ),
            )
        )
        serializer = self.get_serializer(response.data)
        match response.status:
            case EVSendingStatus.SUCCESSFULLY_SENT:
                return Response(serializer.data, status=response.status_code)
            case EVSendingStatus.SENDING_LIMIT_REACHED:
                return Response(
                    {
                        "detail": EVSendingStatus.SENDING_LIMIT_REACHED.message,
                        "retry_after": response.retry_after,
                    },
                    status=response.status_code,
                )


class VerifyUserUpdateAPIView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        return UserEmailVerifierService(request.user, request.data).verify()
