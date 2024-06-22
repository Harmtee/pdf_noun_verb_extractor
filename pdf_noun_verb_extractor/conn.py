# settings.py

from mongoengine import connect
from decouple import config, Csv

ENVIRONMENT = config('DJANGO_ENV', default='development')

# MongoDB settings
MONGODB_SETTINGS = {
    'db': config('DB_NAME', default='pdf_extractor'),
    'host': config('CONNECTION_STRING', default='mongodb://localhost:27017'),         
}

if ENVIRONMENT == 'production':
    # Production-specific settings
    MONGODB_SETTINGS['host'] = config('PRODUCTION_CONNECTION_STRING', default='mongodb://localhost:27017')

elif ENVIRONMENT == 'testing':
    # Testing-specific settings
    MONGODB_SETTINGS['host'] = config('TESTING_CONNECTION_STRING', default='mongodb://localhost:27017')

# Connect to MongoDB using MongoEngine
connect(
    db=MONGODB_SETTINGS['db'],
    host=MONGODB_SETTINGS['host'],
)



