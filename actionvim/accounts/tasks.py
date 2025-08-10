from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task

from actionvim.accounts.models import Account


@shared_task(name="accounts.confirmation_email")
def send_confirmation_email(account_id):
    account = Account.objects.filter(id=account_id).first()
    if not account:
        return

    subject = "Account Confirmation"
    html_content = render_to_string(
        "accounts/confirmation_email.html", {"account": account}
    )
    text_content = strip_tags(html_content)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = account.email

    msg = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[to_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
