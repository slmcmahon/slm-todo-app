from google.appengine.ext import ndb

class TodoItem(ndb.Model):
    creator = ndb.UserProperty(indexed=True)
    text = ndb.StringProperty(indexed=False)
    active = ndb.BooleanProperty(default=True, indexed=True)
    category = ndb.StringProperty(indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    closed_date = ndb.DateProperty(auto_now_add=False)
