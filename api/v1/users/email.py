from djoser.email import PasswordResetEmail as DjoserPasswordResetEmail

from api.common.tasks import send_html_mail


class PasswordResetEmail(DjoserPasswordResetEmail):
    def send(self, to: list[str], *args, **kwargs) -> None:
        context = self.get_context_data()
        user = context["user"]
        send_html_mail.delay(
            subject="Password reset",
            html_email_template_name="email/password_reset.html",
            recipient_list=to,
            context={
                "username": user.username,
                "url": context["url"],
            },
        )
