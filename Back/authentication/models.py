# accounts/models.py
from django.db import models
from django.conf import settings

# this resets everything in the database, we would do this here because we deleted the profile model
# python manage.py migrate authentication zero
