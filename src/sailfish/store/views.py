'''
Created on Aug 29, 2009

@author: Nick
'''
import sys
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from auth.decorators import login_required
import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
from models import Product

def index(request):
    "Index page - show available products"
    return render_to_response('store/index.html', {
        'products': Product.all()
    }, RequestContext(request))
    
#@login_required
#def create(request):
#    "Backdoor to create a new entity"
#    u = auth.get_current_user(request)
#    if u.is_admin:
#        p = Product()
#        p.name = "New Product"
#        p.description = "The description"        
#        p.put()
#    return HttpResponseRedirect(reverse('store-index'))
