'''
Created on Sep 6, 2009

@author: Nick
'''
from django.conf import settings
from django.template.loader import render_to_string


def send_templated_email(subject, template, template_vars, email_to, context=None, email_from=None):
    """Renders template with specified context.
    Email it to specified address.

    @param subject Subject for the email
    @param template Path to template
    @param template_vars Dictionary of variables for the template
    @param email_to Where to send it to
    @param context Context instance (usually RequestContext)
    @param email_from From (if not specified, will use default email)
    """
    email_text = render_to_string(template, template_vars, context)
    email_from = email_from or settings.DEFAULT_FROM_EMAIL
    
    # Google syntax
    from google.appengine.api.mail import send_mail
    send_mail(email_from, email_to, subject, email_text)
    # Django syntax
    # from django.core.mail import send_mail
    #send_mail(subject, message, sender, recipients)
