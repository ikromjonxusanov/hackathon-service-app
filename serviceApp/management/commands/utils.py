from telegram import InlineKeyboardButton
from serviceApp.models import *

def get_object_or_None(ModelName, id):
    try:
        return ModelName.objects.get(id=id)
    except:
        return None

def get_botuser_object_or_None(id):
    try:
        return BotUserModel.objects.get(telegram_id=id)
    except:
        return None



def categoriesR():
    categories = CategoryModel.objects.all()
    keyboard = []
    for item in categories:
        keyboard.append([InlineKeyboardButton(text=item.name, callback_data=f"category/{item.id}")])
    keyboard.append([InlineKeyboardButton(text="Orqaga", callback_data=f"home")])

    return keyboard

def servicesR(c_id):
    category = get_object_or_None(CategoryModel, c_id)
    if category:
        queryset = ServiceModel.objects.filter(category=category)
        keyboard = []
        for item in queryset:
            keyboard.append([InlineKeyboardButton(text=item.name, callback_data=f"service/c-{c_id}/{item.id}")])
        keyboard.append([InlineKeyboardButton(text="Orqaga", callback_data=f"categories")])
        return keyboard
    else:
        return None

def serviceR(c_id, s_id):
    service = get_object_or_None(ServiceModel, s_id)
    if service:
        keyboard = [
            [
                InlineKeyboardButton(text="Orqaga", callback_data=f"category/{c_id}"),
                InlineKeyboardButton(text="Savatga qo'shish", callback_data=f"basket/add/{s_id}")
            ]
        ]
        return keyboard
    else:
        return None

def basketKeyboard(u_id):
    data = basketShowServices(u_id)
    keyboardBasket = []
    for id in data:
        object = ServiceModel.objects.get(id=id)
        keyboardBasket.append([InlineKeyboardButton(text=f"{object}", callback_data=f'{id}/service')])
    if data:
        keyboardBasket.append(
            [
                InlineKeyboardButton(text="Buyurtma berish", callback_data='ordering'),
            ]
        )

    keyboardBasket.append([InlineKeyboardButton(text="Orqaga", callback_data='home')])

    return keyboardBasket
def basketShowServices(u_id):
    filename = 'baskets/'+str(u_id)+".txt"

    try:
        with open(filename, 'r') as f:
            fData=[]
            for item in f:
                fData.append(int(item.rstrip('\n')))
            return fData
    except:
        with open(filename, 'w') as f:
            f.write("")
        return []
def basketAddService(u_id, s_id):
    filename = 'baskets/'+str(u_id)+".txt"
    try:
        with open(filename, 'r') as f:
            fData = f.readlines()
            status = True
            for item in fData:
                if item.rstrip('\n') == str(s_id):
                    status = False
            if status:
                with open(filename, 'a') as fa:
                    fa.write(str(s_id)+"\n")
    except:
        with open(filename, 'w') as fw:
            fw.write(str(s_id)+"\n")

def basketRemoveService(u_id, s_id):
    filename = 'baskets/'+str(u_id)+".txt"
    try:
        with open(filename, 'r') as f:
            fData = f.readlines()
            status = False
            for item in fData:
                if item.rstrip('\n') == str(s_id):
                    fData.remove(item)
                    status = True
            if status:
                with open(filename, 'w') as fa:
                    for item in fData:
                        fa.write(item)
    except:
        with open(filename, 'w') as fw:
            fw.write("")
def basketClearService(u_id):
    filename = 'baskets/'+str(u_id)+".txt"
    with open(filename, 'w') as f:
        f.write("")