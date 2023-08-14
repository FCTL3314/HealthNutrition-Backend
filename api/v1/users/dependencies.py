from dependencies import Injector

from api.v1.users.services import EVAdapter
from api.v1.users.services.email_verification.email_verification_sender import (
    EVSenderService,
)
from api.v1.users.services.email_verification.next_email_sending_time import (
    EVNextSendingTimeService,
)


class EVSenderContainer(Injector):
    email_verification_sender = EVSenderService
    next_sending_time_calculator = EVNextSendingTimeService
    email_verification_adapter = EVAdapter
