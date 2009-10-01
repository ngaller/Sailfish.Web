'''
Created on Aug 29, 2009

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
from models import Product, ProductForm, PaypalRequest, UserProduct

def index(request, *args):
    "Index page - show available products"
    return render_to_response('store/index.html', {
        'products': Product.all()
    }, RequestContext(request))
    
def details_search(request):
    p = Product.get_by_key_name(request.GET["app"], None)
    if not p:
        raise Http404("Product cannot be found")
    return render_to_response('store/details.html', 
                              { 'p': p }, 
                              RequestContext(request))
    
def details(request, id):
    p = Product.get(id)
    if not p:
        raise Http404("Product cannot be found")
    return render_to_response('store/details.html', 
                              { 'p': p },
                              RequestContext(request))
    
@login_required    
def purchase_search(request):
    return purchase_do(request, Product.get_by_key_name(request.GET["app"], None))
    
@login_required    
def purchase(request, id):
    return purchase_do(request, Product.get(id))
    
class PurchaseForm(forms.Form):
    email = forms.EmailField(help_text="Email for your confirmation message")
    pin = forms.RegexField(max_length=8, 
                           help_text="You can find the pin under Options > Status > PIN",
                           regex="[A-Za-z0-9]{8}")

def purchase_do(request, product):
    if not product:
        raise Http404("Product cannot be found")
    if UserProduct.get_product(auth.get_current_user(request), product):
        return render_to_response('store/details.html', 
                                  {'p': product, 
                                   'msg': "You already own this application - to associate with a different device please contact support or use another account."},
                                   RequestContext(request))
    if request.method == "POST":
        form = PurchaseForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pin = data["pin"]
            email = data["email"]
            user = auth.get_current_user(request)
            user.preferred_email = email
            user.put()
        else:
            return render_to_response('store/purchase_info.html', 
                                      { 'form': form },
                                      RequestContext(request)) 
    else:
        pin = request.GET.get("pin", None)
        email = auth.get_current_user(request).preferred_email
    if not (pin and email):
        form = PurchaseForm(data={'email': email, 'pin': pin})
        return render_to_response('store/purchase_info.html', 
                                  { 'form': form, 'product': product },
                                  RequestContext(request))        
    tx = PaypalRequest.prepare(product, auth.get_current_user(request), pin)
    return render_to_response('store/purchase.html', 
                              {'product': product, 
                               'pin': pin, 
                               'txid': tx.key() },
                              RequestContext(request))
    
def paypal_ipn(request):
    """
    Make sure this is a valid request, and activate the corresponding record.
    The transaction id is passed as a custom variable.
    """
    if PaypalRequest.validate_ipn(request):
        def tran():
            #tx = PaypalRequest.get_by_id(request.POST["item_number"])
            tx = PaypalRequest.get(request.POST["custom"])
            if not tx:
                raise Http404("Transaction not found")
            return tx.process_ipn(request)
        userprod = db.run_in_transaction(tran)
        if userprod:
            userprod.send_thankyou_mail()
    return HttpResponse("OK", mimetype="text/plain")

def thankyou(request, txid):
    tx = PaypalRequest.get(txid)
    if not tx:
        raise Http404("Transaction not found")    
    return render_to_response('store/thankyou.html', 
                              { 'tx' : tx }, 
                              RequestContext(request))

def activate(request):
    """
    Make sure the user has the product (identify using PIN), and return
    activation code.
    """
    pin = request.GET['pin']
    p = Product.get_by_key_name(request.GET["app"], None)
    if not p:
        raise Http404("Product not found")
    userproduct = UserProduct.gql("where pin = :1 and product = :2", 
                                  pin, p).get()
    if not userproduct:
        raise Http404("Activation data not found")
    return HttpResponse(userproduct.get_activation_code(), mimetype='text/plain')
    

@login_required
def create(request, keyname):
    "Backdoor to create a new entity"
    u = auth.get_current_user(request)
    if u.is_admin:
        p = Product(key_name=keyname)
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
        if not p:
            raise Http404("Product cannot be found") 
        elif request.method == "POST":
            form = ProductForm(data=request.POST, instance=p)            
            if form.is_valid():
                form.save()
        else:
            form = ProductForm(instance=p)
            return render_to_response('store/edit.html', 
                                      { 'form': form },
                                      RequestContext(request))
    return HttpResponseRedirect(reverse('store-index'))    
    
