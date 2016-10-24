from google.appengine.ext import ndb
import datetime


class TodoItem(ndb.Model):
    creator = ndb.UserProperty(indexed=True)
    text = ndb.StringProperty(indexed=False)
    active = ndb.BooleanProperty(default=True, indexed=True)
    category = ndb.StringProperty(indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    closed_date = ndb.DateTimeProperty(auto_now_add=False)


class TodoManager():

    @staticmethod
    def add_todo(user, text, category=None):
        todo = TodoItem()
        todo.creator = user
        todo.text = text
        todo.category = category if category else 'General'
        todo.put()

    @staticmethod
    def get_todo_items(user):
        qry = TodoItem.query(TodoItem.creator == user and TodoItem.active == True)
        return qry.fetch(limit=None)

    @staticmethod
    def close_todo(key):
        k = ndb.Key(urlsafe=key)
        qry = TodoItem.query(ancestor=k)
        todo = qry.fetch(1)[0]
        todo.closed_date = datetime.datetime.now()
        todo.active = False
        todo.put()

    @staticmethod
    def delete_todo(key):
        k = ndb.Key(urlsafe=key)
        k.delete()


