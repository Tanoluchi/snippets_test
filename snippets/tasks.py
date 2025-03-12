from celery import shared_task
from django.core.mail import send_mail

from django_snippets.settings import EMAIL_HOST_USER as sender

@shared_task(bind=True)
def sendEmailInSnippetCreation(self, snippet_name, snippet_description, user_mail):
    """
        Celery task to send an email notification when a snippet is created.

        This task sends an email to the user who created a snippet, confirming its successful creation.

        Parameters:
        - snippet_name (str): The name of the snippet created.
        - snippet_description (str): The description of the snippet.
        - user_mail (str): The email address of the user who created the snippet.

        Behavior:
        - If a user email is provided, the function constructs an email with the snippet details.
        - Sends an email with the subject `"Snippet <snippet_name> created successfully"` from the configured sender email.
        - The email body contains the snippet name and its description.

        Returns:
        - None (the task executes asynchronously via Celery).
    """
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
