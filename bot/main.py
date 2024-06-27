import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv

from const import NEW_EMPLOYEE, OLD_EMPLOYEE, MOSCOW_NO, MOSCOW_YES

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')


def start_handler(update, context):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton(
            'Я новый сотрудник',
            callback_data=NEW_EMPLOYEE)],
        [InlineKeyboardButton(
            'Я работаю здесь уже долгое время',
            callback_data=OLD_EMPLOYEE)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Для начала, расскажите, вы новый сотрудник или уже давно с нами?',
        reply_markup=reply_markup)


def moscow_office_handler(update, context):
    """Обработчик кнопок про Москву"""
    query = update.callback_query
    query.answer()

    if query.data == NEW_EMPLOYEE:
        text = ('Добро пожаловать в ГК QTECH!! Этот чат-бот поможет '
                'сориентироваться в первые дни работы '
                'и узнать больше о нашей компании. '
                'Посещаете ли вы офис в Москве?')
    elif query.data == OLD_EMPLOYEE:
        text = ('Здорово, что вы присоединились к чат-боту! '
                'Он поможет вам структурировать  информацию '
                'о нашей компании воедино или узнать что-то новое. '
                'Вы сможете задать свои вопросы и озвучить '
                'предложения по улучшению. '
                'Посещаете ли вы офис в Москве?')

    keyboard = [
        [
            InlineKeyboardButton('Да', callback_data=MOSCOW_YES),
            InlineKeyboardButton('Нет', callback_data=MOSCOW_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=text, reply_markup=reply_markup)


def info_buttons_handler(update, context):
    """Обработчик нажатия кнопок"""
    query = update.callback_query
    query.answer()

    if query.data == MOSCOW_YES:
        keyboard = [
            [
                InlineKeyboardButton(
                    'Кнопка посещающих Москву',
                    callback_data='moscow_button')
            ]
        ]
    elif query.data == MOSCOW_NO:
        keyboard = [
            [
                InlineKeyboardButton(
                    'Кнопка для не посещающих Москву',
                    callback_data='no_moscow_button')
            ]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text='Спасибо за информацию! '
             'Предлагаем вам ознакомиться с меню '
             'и выбрать интересующую категорию',
        reply_markup=reply_markup)


def main():
    """Основная функция для запуска бота"""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CallbackQueryHandler(
        moscow_office_handler,
        pattern='^(new_employee|old_employee)$'))
    dispatcher.add_handler(
        CallbackQueryHandler(info_buttons_handler,
                             pattern='^(moscow_yes|moscow_no)$'))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
