'''
Created on Aug 29, 2009

@author: Nick
'''
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from auth.models import UserProfile
import logging
import settings
import urllib2
import utils

class Product(db.Model):
    """
    Represents a product in the catalog.
    """
    name = db.StringProperty()
    description = db.TextProperty()
    price = db.FloatProperty()
    icon = db.StringProperty()
    download_url = db.StringProperty()
    # Secret used for activation
    secret = db.StringProperty()
    # if this is False product will only be shown for Admin
    available = db.BooleanProperty()
    
    def is_freeware(self):
        return self.price == 0
        
class ProductForm(djangoforms.ModelForm):
    class Meta:
        model = Product
        
class UserProduct(db.Model):
    user = db.Reference(UserProfile)
    product = db.Reference(Product)
    pin = db.StringProperty()
    purchase_date = db.DateTimeProperty()
    
    def __init__(self, tx):
        super(UserProduct, cls).__init__(self, tx)
        self.user = tx.user
        self.product = tx.product
        self.purchase_date = tx.txdate
        self.pin = tx.pin
        
    def send_thankyou_mail(self):
        """
        Called after IPN.  Send a confirmation to the user.
        """
        utils.send_templated_email("Your Sailfish Mobile purchase confirmation", 
                                   "store/thankyou_mail.txt", 
                                   { 'userproduct': self,
                                     'tx': self.parent() })
    
    @classmethod
    def has_product(cls, user, product):
        """
        True if the specified user already has a record for the product.
        """
        pass
        
class PaypalRequest(db.Model):
    """
    Stores a paypal request awaiting confirmation.
    """
    user = db.Reference(UserProfile)
    product = db.Reference(Product)
    txdate = db.DateTimeProperty(auto_now_add=True)
    txnid = db.StringProperty()
    amount = db.FloatProperty()
    pin = db.StringProperty()
    status = db.StringProperty()    
    
    def process_ipn(self, request):
        """
        Process the given IPN request (must have been already validated)
        This should be run within a transaction.
        """
        if self.status == "PENDING" and \
            request.POST["payment_status"] == "Completed" and \
            request.POST["payment_gross"] == amount:
            userprod = UserProduct(self)
            userprod.put()
            self.status = "COMPLETE"
            self.txnid = request.POST["txn_id"]
            self.put()
            return userprod
        return None
            
    
    @classmethod
    def prepare(cls, product, user, pin):
        """
        Save and return request to the database with current user and 
        designated product.
        """
        tx = PaypalRequest()
        tx.user = user
        tx.product = product
        tx.amount = product.price
        tx.pin = pin
        tx.status = "PENDING"
        tx.put()
        return tx
    
    @classmethod
    def validate_ipn(cls, request):
        """
        Validate the given request with Paypal.
        Return true if valid.
        """
        if settings.DEBUG:
            base_url = "https://www.sandbox.paypal.com/cgi-bin/webscr"
        else:
            base_url = "https://www.paypal.com/cgi-bin/webscr"
        data = "cmd=_notify-validate&" + request.raw_post_data
        response = urllib2.urlopen(base_url, data)
        response_data = response.read()
        if response_data == "VERIFIED":
            logging.info("Valid IPN data: ")
            for (k,v) in request.POST.items():
                logging.info(k + " = " + v)
            return True
        else:
            logging.warn("Invalid IPN data: " + 
                         "Post = [" + request.raw_post_data + "]; " + 
                         "Response = [" + response_data + "]")
            return False
        
        