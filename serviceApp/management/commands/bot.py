from django.core.management.base import BaseCommand, CommandError
import logging
from django.conf import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, ConversationHandler, CallbackContext, CommandHandler, MessageHandler ,CallbackQueryHandler, CallbackContext
from telegram.utils.request import Request

from serviceApp.models import BotUserModel, ServiceModel, OrderModel


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            raise e
    return inner

@log_errors
def do_echo(update: Update, context: CallbackContext):
    text = update.message.text

    reply_text = text
    update.message.reply_text(
        text=reply_text,
    )

def registerContact(update, context):
    u = update.message
    print(u.from_user.id, u.from_user.first_name,u.from_user.last_name,u.contact.phone_number)
    if len(u.contact.phone_number) == 13:
        u.reply_text(f'Enter your first name')
        


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    
    update.message.reply_text(f'Welcome, Please register!')
    reply_markup = ReplyKeyboardMarkup([[ KeyboardButton('Share contact', request_contact=True) ]], resize_keyboard = True)
    update.message.reply_text('Enter your phone number',reply_markup=reply_markup)
    return 1

def Name(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    
    update.message.reply_text(f'Enter your first name')

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

        conv_handler = ConversationHandler(
            entry_points = [CommandHandler('start', start)],
            states = {
                1: {
                    MessageHandler(Filters.contact, registerContact)
                },
                2: {
                    MessageHandler(Filters.text, Name)
                }
            },
            fallbacks =[MessageHandler(Filters.text, start)]

        )

        updater.dispatcher.add_handler(conv_handler)

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