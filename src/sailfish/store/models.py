'''
Created on Aug 29, 2009

@author: Nick
'''
from google.appengine.ext import db

class Product(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    price = db.FloatProperty()
    icon = db.StringProperty()
    download_url = db.StringProperty()
    
    def is_freeware(self):
        return self.price == 0
        
    