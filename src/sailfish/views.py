'''
Created on Aug 29, 2009

@author: Nick
'''
import sys
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from datetime import datetime

class ContactForm(forms.Form):
    name = forms.CharField(max_length=64)
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            send_email(form.cleaned_data)
            return HttpResponseRedirect('/thanks.html')
    else:
        form = ContactForm()
    return render_to_response('contact.html', {
        'form': form,
    }, RequestContext(request))

def send_email(data):
    subject = "Sailfish.mobi contact form"
    message = "Contact from " + data["name"] + "\n\n" + data["comments"]
    sender = data["email"]
    recipients = ["contact@sailfish.mobi"]
    from django.core.mail import send_mail
    send_mail(subject, message, sender, recipients)
