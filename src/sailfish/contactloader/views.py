'''
Created on Sep 7, 2009

@author: Nick
'''
import sys, logging
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from auth.decorators import login_required
from google.appengine.ext import db
import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from sailfish.store.models import Product, UserProduct
from models import ImportList

class CsvFileField(forms.FileField):
    def clean(self, data, initial=None):
        data = super(CsvFileField, self).clean(data, initial)
        if not data.name.lower().endswith(".csv"):
            raise forms.util.ValidationError("File should be a CSV file")
        return data

class UploadForm(forms.Form):
    file = CsvFileField(help_text="Select the file to upload (should be a CSV file smaller than 1 mb)",)

@login_required
def index(request):
    user = auth.get_current_user(request)
    product = Product.get_by_key_name("ContactLoader")
    lst = None
    form = None
    reg = UserProduct.get_product(user, product)
    if reg:            
        if request.method == "POST":
            form = handle_upload(request)
        else:
            form = UploadForm()
        lst = ImportList.gql("where user = :1", user).get()
    return render_to_response('contactloader/index.html', 
                              {'lst': lst, 
                               'reg': reg, 
                               'product': product,
                               'form': form },
                              RequestContext(request))

def handle_upload(request):
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        user = auth.get_current_user(request)
        q = ImportList.gql("where user = :1", user)
        for result in q:
            result.delete()
        lst = ImportList()
        lst.user = user
        lst.data = request.FILES['file'].read()
        lst.put()     
    return form   
    
def download(request):
    user = auth.get_current_user(request)    
    if not user:
        pin = request.GET["pin"].upper()
        code = request.GET["code"]
        product = Product.get_by_key_name("ContactLoader")
        userproduct = UserProduct.gql("where product = :1 and pin = :2", 
                                      product, pin).get()
        if not userproduct or not userproduct.validate_code(code):
            raise Http404("Could not find activation data")
        user = userproduct.parent()
    lst = ImportList.gql("where user = :1", user).get()
    if not lst:
        raise Http404("No list has been uploaded on the account yet")
    return HttpResponse(lst.data, "text/csv")
    
