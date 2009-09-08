'''
Created on Sep 7, 2009

@author: Nick
'''
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from auth.models import UserProfile
import logging
import settings

class ImportList(db.Model):
    """
    Import List - parent = user
    """
    user = db.Reference(UserProfile)
    upload_date = db.DateProperty(auto_now_add=True)
    data = db.BlobProperty()