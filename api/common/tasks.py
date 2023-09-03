from celery import shared_task

from api.common import mail

send_mail = shared_task(mail.send_mail)
send_html_mail = shared_task(mail.send_html_mail)
