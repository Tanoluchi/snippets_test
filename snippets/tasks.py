from celery import shared_task
from django.core.mail import send_mail

from django_snippets.settings import EMAIL_HOST_USER as sender

@shared_task(bind=True)
def sendEmailInSnippetCreation(self, snippet_name, snippet_description, user_mail):
    if user_mail:
        subject = 'Snippet "' + snippet_name + '" created successfully'
        body = (
            'The snippet "' + snippet_name + '" was created with the following description: \n'
            + snippet_description
        )
        send_mail(
            subject=subject,
            message=body,
            from_email=sender,
            recipient_list=[user_mail],
            fail_silently=False,
        )
