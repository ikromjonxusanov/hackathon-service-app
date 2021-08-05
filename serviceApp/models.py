from django.db.models import *
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class BotUserModel(Model):
    telegram_id = IntegerField(unique=True)
    first_name = CharField(max_length=60)
    last_name = CharField(max_length=60)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.first_name + " " + self.last_name

class CategoryModel(Model):
    name = CharField(max_length=255)
    def __str__(self):
        return self.name

class ServiceModel(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='service', default='default-service.png')
    price = FloatField()
    description = TextField()
    category = ForeignKey(CategoryModel, on_delete=SET_NULL, null=True)
    def __str__(self):
        return self.name

class OrderModel(Model):
    user = ForeignKey(BotUserModel, on_delete=CASCADE)
    service = ManyToManyField(ServiceModel)
    date = DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name+f" --- {self.date}"

class CommentModel(Model):
    user = ForeignKey(BotUserModel, on_delete=CASCADE)
    text = TextField()
    def __str__(self):
        return f"{self.user.first_name} {self.text}"