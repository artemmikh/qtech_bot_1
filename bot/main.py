import os

from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv

load_dotenv()

updater = Updater(token=os.getenv('BOT_TOKEN'))


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Для начала, расскажите, вы новый сотрудник или уже давно с нами?')


if __name__ == '__main__':
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.start_polling()
    updater.idle()
