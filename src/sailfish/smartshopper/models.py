'''
Created on Oct 22, 2009

@author: Nick
'''

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from auth.models import UserProfile
from sailfish.store.models import UserProduct
import logging
import settings

class SmartShopperList(db.Model):
    name = db.StringProperty()
    # Common properties used for sync
    owner = db.ReferenceProperty(UserProfile)
    updated_by = db.ReferenceProperty(UserProduct)
    version = db.IntegerProperty()
    global_id = db.IntegerProperty()
    purged = db.BooleanProperty()
    
    @classmethod
    def get_lists_for_user(cls, user):
        '''
        All lists accessible to the specified user are returned.
        '''
        pass
    
    def is_accessible(self, user):
        '''
        Return true if and only if the specified user can access this
        list.
        '''
        return owner == user
    
    def add_item(self, user, category, name, updated_by):
        '''
        Create a matching item template, if needed.
        Then add it to the list.
        '''
        template = SmartShopperItemTemplate.find_or_create(category, name)
        item = SmartShopperListItem(parent_list=self,
                                    template=template,
                                    owner=user,)
    
    def remove_item(self, user, item_id):
        '''
        Remove specified item (mark it as purged)
        '''
        item = SmartShopperListItem.get(item_id)
        if item.parent_list.key() == self.key():
            item.purged = True
    
    def complete_item(self, user, item_id):
        '''
        Mark specified item as complete
        '''
        item = SmartShopperListItem.get(item_id)
        if item.parent_list.key() == self.key():
            item.completed = True

class SmartShopperListItem(db.Model):
    parent_list = db.ReferenceProperty(SmartShopperList)
    template = db.ReferenceProperty(SmartShopperListItem)
    # Common properties used for sync
    owner = db.ReferenceProperty(UserProfile)
    updated_by = db.ReferenceProperty(UserProduct)
    version = db.IntegerProperty()
    global_id = db.IntegerProperty()    
    purged = db.BooleanProperty()

class SmartShopperItemTemplate(db.Model):
    name = db.StringProperty()
    category = db.StringProperty()
    # Common properties used for sync
    owner = db.ReferenceProperty(UserProfile)
    updated_by = db.ReferenceProperty(UserProduct)
    version = db.IntegerProperty()
    global_id = db.IntegerProperty()
    purged = db.BooleanProperty()
