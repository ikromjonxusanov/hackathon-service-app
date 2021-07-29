from django.db.models import *

# Create your models here.

class BotUserModel(Model):
    telegram_id = IntegerField()


