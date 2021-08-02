from django.db.models import *
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class BotUserModel(Model):
    telegram_id = CharField(max_length=25, unique=True)
    first_name = CharField(max_length=60)
    last_name = CharField(max_length=60)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.first_name + " " + self.last_name

class ServiceModel(Model):
    name = CharField(max_length=255)
    price = FloatField()
    description = TextField()
    def __str__(self):
        return self.name

class OrderModel(Model):
    user = ForeignKey(BotUserModel, on_delete=CASCADE)
    service = ForeignKey(ServiceModel, on_delete=CASCADE)
    date = DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " --- " + str(self.date)