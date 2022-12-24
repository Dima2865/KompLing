from mongoengine import Document, StringField, IntField, FloatField, DateTimeField, ListField, ReferenceField, DoesNotExist
DEFAULT_DATABASE = "news_db"

class Article(Document):
    meta = {"db_alias": DEFAULT_DATABASE}

    url = StringField(required=True, unique=True)
    title = StringField(required=True)
    content = ListField(StringField(), required=True)
    author = StringField()
    date = DateTimeField(required=True)