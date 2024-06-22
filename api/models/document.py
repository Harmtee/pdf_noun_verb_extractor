from mongoengine import Document, StringField, ListField, DateTimeField, EmailField

class PDF(Document):
    content = StringField()
    src = StringField()
    client_name = StringField()
    upload_date = DateTimeField()
    nouns = ListField(StringField())
    verbs = ListField(StringField())
    email = EmailField(required=True, unique=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.client_name
