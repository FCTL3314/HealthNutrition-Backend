from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def convert_html_to_email_message(html_email_template_name, context):
    message = render_to_string(html_email_template_name, context)
    return EmailMultiAlternatives(body=message)
