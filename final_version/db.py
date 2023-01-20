from mongoengine import Document, StringField, IntField, FloatField, DateTimeField, ListField
DEFAULT_DATABASE = "news_db"


class Article(Document):
    meta = {"db_alias": DEFAULT_DATABASE}

    url = StringField(required=True, unique=True)
    title = StringField(required=True)
    content = ListField(StringField(), required=True)
    author = StringField()
    date = DateTimeField(required=True)
    sentence = ListField(StringField())
    tonality = ListField(FloatField())
    sentence_count = IntField(default=0)

    @property
    def text(self):
        return " ".join(self.content)

    @property
    def internal_url(self) -> str:
        """Возвращает url страницы статьи в интерфейсе"""

        return f'/articles/{self.id}'

    @property
    def sentence_tonality(self):
        for text, tone in zip(self.sentence, self.tonality):
            yield text, tone

    def clean(self):
        super().clean()

        if self.sentence:
            self.sentence_count = len(self.sentence)
