from serviceApp.management.commands.utils import *
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import InlineKeyboardButton,  InlineKeyboardMarkup, KeyboardButton, Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters,  CommandHandler, MessageHandler ,CallbackQueryHandler, CallbackContext
from telegram.utils.request import Request
from serviceApp.models import *


keyboard = [
    [
        InlineKeyboardButton("🗂 Xizmat toifalari", callback_data='categories'),
        InlineKeyboardButton("📦 Mening buyurmalarim", callback_data='orders'),
    ],
    [
        InlineKeyboardButton("🛒 Savat", callback_data='Basket'),
        InlineKeyboardButton("✉️ Izoh qoldirish", callback_data='comments')
    ],
]
echoIn = None
homeMsg = "<b>Akfa Service Bot</b>"
userFullName = {"users":[]}

def start(update: Update, context: CallbackContext) -> None:
    global keyboard, homeMsg, echoIn
    user_id = update.message.from_user.id

    bUser = get_botuser_object_or_None(user_id)
    print(bUser)
    if bUser != None:
        update.message.reply_html(f'<b>Assalamu Alaykum {homeMsg} xush kelibsiz</b>', reply_markup=InlineKeyboardMarkup(keyboard))
    else:#1176483954
        echoIn = "first_name"
        update.message.reply_text('Ismingizni kiriting')



def echo(update: Update, context: CallbackContext) -> None:
    global echoIn, keyboard, userFullName
    msg = update.message.text
    user_id = update.message.from_user.id

    if echoIn == "feedback":
        user = BotUserModel.objects.get(telegram_id=user_id)
        comment = CommentModel(user=user, text=msg)
        comment.save()
        update.message.reply_html("<b>Izohingiz uchun rahmat !!!</b>", reply_markup=InlineKeyboardMarkup(keyboard))
        echoIn = None
    elif echoIn == "first_name":
        userFullName['users'].append([user_id, {'first_name':msg}])
        echoIn = "last_name"
        update.message.reply_text("Familiyangizni kiriting")
    elif echoIn == "last_name":
        USER = False
        for user in userFullName['users']:
            if user[0] == user_id:
                USER = user
        if USER:
            USER[1]['last_name'] = msg
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Share contact', request_contact=True)]],
                                               resize_keyboard=True)
            echoIn = None
            update.message.reply_text('Telefon nomeringizni yuboring', reply_markup=reply_markup)

def service(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    global keyboard, echoIn, homeMsg
    if query.data.split('/')[0] == 'basket':
        if query.data.split('/')[1] == 'add':
            id = int(query.data.split('/')[2])
            basketAddService(query.from_user.id, id)
            object = ServiceModel.objects.get(id=id)
            query.answer(text=f'{object} savatga qo\'shildi ✅', show_alert=True)
    else:
        query.answer()
        query.delete_message()
    if query.data == "home":
        query.message.reply_html(text=homeMsg, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "categories":
        keyboardCategories = categoriesR()
        query.message.reply_text(text="🗂 Xizmat toifasini tanlang", reply_markup=InlineKeyboardMarkup(keyboardCategories))
    elif query.data.split('/')[0] == "category":
        id = int(query.data.split('/')[1])
        keyboardServices = servicesR(id)
        query.message.reply_text(text="🗂 Xizmat tanlang", reply_markup=InlineKeyboardMarkup(keyboardServices))
    elif query.data.split('/')[0] == "service":
        id = int(query.data.split('/')[2])
        c_id = int(query.data.split('/')[1].split('-')[1])
        object = ServiceModel.objects.get(id=id)
        image = open(str(settings.MEDIA_ROOT)+"/"+str(object.image), 'rb')
        keyboardService = serviceR(c_id=c_id, s_id=id)
        query.message.reply_photo(photo=image, caption=f"<b>{object}</b>\n{object.description}\n💵{object.price} so'm", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboardService))
    elif query.data == 'Basket':
        keyboardBasket = basketKeyboard(query.from_user.id)
        msg = None
        if len(keyboardBasket) > 1:
            msg = "<b>🛒 Savat</b>"
        else:
            msg = "<b>🛒 Savat</b> <i>(Hozircha <b>savat</b>da hech narsa yo'q</i>"

        query.message.reply_html(msg, reply_markup=InlineKeyboardMarkup(keyboardBasket))
    elif query.data == 'ordering':
        user_id = query.from_user.id
        basketServices = basketShowServices(user_id)
        user = BotUserModel.objects.get(id=1)

        order = OrderModel(user=user)
        if basketServices:
            order.save()
            for pk in basketServices:
                s = ServiceModel.objects.get(id=pk)
                order.service.add(s)
            basketClearService(user_id)
        query.message.reply_html(homeMsg, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "orders":
        user_id = query.from_user.id
        user = BotUserModel.objects.get(telegram_id=user_id)
        orders = user.ordermodel_set.order_by('-id')
        for object in orders:
            msg = f"<b>📦 Order -{object.id}</b>"
            i = 0
            for itemObject in object.service.all():
                i+=1
                msg += f"\n<b>{i}</b> - {itemObject}"
            query.message.reply_html(msg)
        key = [
            [
                InlineKeyboardButton('Orqaga', callback_data='home')
            ]
        ]
        query.message.reply_html("<b>Orqaga</b>", reply_markup=InlineKeyboardMarkup(key))
    elif query.data == "comments":
        echoIn = "feedback"
        query.message.reply_html(f"✉️ {homeMsg}ga izohingizni qoldiring!!!")
    elif query.data.split('/')[1] == 'service':
        id = int(query.data.split('/')[0])
        object = ServiceModel.objects.get(id=id)
        image = open(str(settings.MEDIA_ROOT) + "/" + str(object.image), 'rb')
        keyboardBasketService = [
            [
                InlineKeyboardButton('❌ Bekor qilish', callback_data=f'remove/{id}'),
                InlineKeyboardButton("⬅️ Orqaga", callback_data="Basket")
            ]
        ]
        query.message.reply_photo(photo=image, caption=f"<b>{object}</b>\n{object.description}\n💵{object.price} so'm",
                                  parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboardBasketService))
    elif query.data.split('/')[0] == 'remove':
        id = int(query.data.split('/')[1])
        user_id = query.from_user.id
        basketRemoveService(u_id=user_id, s_id=id)
        keyboardBasket = basketKeyboard(user_id)
        msg = None
        if len(keyboardBasket) > 1:
            msg = "<b>🛒 Savat</b>"
        else:
            msg = "<b>🛒 Savat</b> <i>(Hozircha <b>savat</b>da hech narsa yo'q</i>"

        query.message.reply_html(msg, reply_markup=InlineKeyboardMarkup(keyboardBasket))

def registerContact(update, context):
    global keyboard, userFullName
    u = update.message
    user_id = u.from_user.id
    user = get_botuser_object_or_None(u.from_user.id)
    if not user:
        USER = False
        for user in userFullName['users']:
            if user[0] == user_id:
                USER = user
        if USER:
            botUser = BotUserModel(
                telegram_id=u.from_user.id,
                first_name=USER[1]['first_name'],
                last_name=USER[1]['last_name'],
                phone_number=u.contact.phone_number
            )
            botUser.save()

    update.message.reply_text(f'Assalamu alaykum', reply_markup=InlineKeyboardMarkup(keyboard))

class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )

        bot = Bot(
            request=request,
            token = settings.TOKEN,
            base_url = settings.PROXY_URL,
        )

        updater = Updater(
            bot=bot,
            use_context= True,
        )
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CallbackQueryHandler(service))
        updater.dispatcher.add_handler(MessageHandler(Filters.contact, registerContact))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.start_polling()
        updater.idle()


#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# keyboard = [
#     [
#         InlineKeyboardButton("Xizmatlar", callback_data='services'),
#         InlineKeyboardButton("Mening Buyurtmalarim", callback_data='orders'),
#     ],
#     [InlineKeyboardButton("Izoh qoldirish", callback_data='comments')],
# ]

# def start(update: Update, context: CallbackContext) -> None:
#     """Sends a message with three inline buttons attached."""
#     global keyboard

#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     update.message.reply_text(f'Assalomu alaykum bla bla bla {}', reply_markup=reply_markup)


# def service(update: Update, context: CallbackContext) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
#     global keyboard

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#     if query.data == "services":
#         services = loadService()
#         keyboardService = []
#         for service in services:
#             keyboardService.append([InlineKeyboardButton(
#                 f"{service['name']}",  callback_data=f"service/{service['id']}")])

#         query.edit_message_text(text=f"Xizmatlar bo'limi", reply_markup=InlineKeyboardMarkup(keyboardService))
#     if query.data.split('/')[0] == 'service':
#         id = int(query.data.split('/')[1])
#         service = loadService(id)
#         keyboardServiceDetail = [
#             [
#                 InlineKeyboardButton("Orqaga", callback_data='services'),
#                 InlineKeyboardButton("Buyurma qilish", callback_data='order'),
#             ]
#         ]
#         query.edit_message_text(text=f"{service['name']}\n{service['description']}\nprice: {service['price']}",
#             reply_markup=InlineKeyboardMarkup(keyboardServiceDetail)
#         )


# def help_command(update: Update, context: CallbackContext) -> None:
#     """Displays info on how to use the bot."""
#     update.message.reply_text("Use /start to test this bot.")


# def main() -> None:
#     """Run the bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater(token)

#     updater.dispatcher.add_handler(CommandHandler('start', start))
#     updater.dispatcher.add_handler(CallbackQueryHandler(service))
#     updater.dispatcher.add_handler(CommandHandler('help', help_command))

#     # Start the Bot
#     updater.start_polling()

#     # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT
#     updater.idle()


# if __name__ == '__main__':
#     main()