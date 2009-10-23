'''
Created on Oct 22, 2009

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
from datetime import datetime
from models import SmartShopperList, SmartShopperListItem

@login_required
def index(request, *args):
    "Index page - show available lists"
    return render_to_response('smartshopper/index.html', {
        'lists': SmartShopperList
            .get_lists_for_user(auth.get_current_user(request)) 
    }, RequestContext(request))
    
@login_required    
def create(request):
    "Create the list - this is invoked from the index form"
    if(request.method != "POST"):
        return index(request)
    name = request.POST["name"]
    if not name:
        return index(request)
    user = auth.get_current_user(request)
    lst = SmartShopperList(name=name, owner = user)
    lst.put()
    return HttpResponseRedirect(reverse('smartshopper-details', lst.key()))
    
@login_required    
def details(request, list_id):    
    lst = SmartShopperList.get(list_id)
    if not lst or not lst.is_accessible(auth.get_current_user(request)):        
        raise Http404("List cannot be found (or it has not been shared with you)")
    return render_to_response('smartshopper/details.html', {
        'lst': lst
    }, RequestContext(request)) 

@login_required
def add_item(request, list_id):
    lst = SmartShopperList.get(list_id)
    if not lst or not lst.is_accessible(auth.get_current_user(request)):        
        raise Http404("List cannot be found (or it has not been shared with you)")
    if request.method != "POST":
        return details(request, list_id)
    category = request.POST["category"]
    name = request.POST["name"]
    lst.add_item(category, name)
    return HttpResponseRedirect(reverse('smartshopper-details', lst.key()))

@login_required
def remove_item(request, list_id, item_id):
    lst = SmartShopperList.get(list_id)
    if not lst or not lst.is_accessible(auth.get_current_user(request)):        
        raise Http404("List cannot be found (or it has not been shared with you)")
    lst.remove_item(item_id)
    return HttpResponseRedirect(reverse('smartshopper-details', lst.key()))

def complete_item(request, list_id, item_id):
    lst = SmartShopperList.get(list_id)
    if not lst or not lst.is_accessible(auth.get_current_user(request)):        
        raise Http404("List cannot be found (or it has not been shared with you)")
    lst.complete_item(item_id)
    return HttpResponseRedirect(reverse('smartshopper-details', lst.key()))