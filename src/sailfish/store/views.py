'''
Created on Aug 29, 2009

@author: Nick
'''
import sys, logging
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from auth.decorators import login_required
import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from datetime import datetime
from models import Product, ProductForm

def index(request):
    "Index page - show available products"
    return render_to_response('store/index.html', {
        'products': Product.all()
    }, RequestContext(request))
    
#class ProductForm(forms.Form):
#    name = forms.CharField(max_length=64)
#    price = forms.FloatField()
#    icon = forms.CharField(max_length=64)
#    download_url = forms.URLField()
#    description = forms.CharField(widget=forms.Textarea)
    
@login_required
def create(request):
    "Backdoor to create a new entity"
    u = auth.get_current_user(request)
    if u.is_admin:
        p = Product()
        p.name = "New Product"
        p.description = "The description"        
        p.put()        
        return HttpResponseRedirect(reverse('store-edit', args=(p.key(),)))
    return HttpResponseRedirect(reverse('store-index'))

@login_required
def edit(request, id):
    u = auth.get_current_user(request)
    if u.is_admin:
        p = Product.get(id)
        if request.method == "POST":
            form = ProductForm(data=request.POST, instance=p)            
            if form.is_valid():
                form.save()
#                data = form.cleaned_data                
#                p.name = data['name']
#                p.price = data['price']
#                p.icon = data['icon']
#                p.description = data['description']
#                p.download_url = data['download_url']
#                p.save()
        else:
            form = ProductForm(instance=p)
            return render_to_response('store/edit.html', 
                                      { 'form': form },
                                      RequestContext(request))
    return HttpResponseRedirect(reverse('store-index'))    
    
