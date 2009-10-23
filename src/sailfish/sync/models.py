'''
Created on Oct 22, 2009

@author: Nick
'''
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from auth.models import UserProfile
from sailfish.store.models import Product, UserProduct
import logging
import settings
import urllib2
from sailfish.utils import send_templated_email

