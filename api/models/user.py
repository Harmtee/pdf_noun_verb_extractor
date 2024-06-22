from mongoengine import Document, StringField, EmailField, ObjectIdField

class User(Document):
    name = StringField()
    email = EmailField(required=True, unique=True)
    
    def __str__(self):
        return self.email
