import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')


# методы, обрабатывающие обновления (например, команды от пользователя),
# принимают два обязательных аргумента: update и context.
def start(update, context):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton(
            'Я новый сотрудник',
            callback_data='new_employee')],
        [InlineKeyboardButton(
            'Я работаю здесь уже долгое время',
            callback_data='old_employee')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Для начала, расскажите, вы новый сотрудник или уже давно с нами?',
        reply_markup=reply_markup)


def moscow_office(update, context):
    """Обработчик кнопок про Москву"""
    query = update.callback_query
    query.answer()

    if query.data == 'new_employee':
        text = ('Добро пожаловать в ГК QTECH!! Этот чат-бот поможет '
                'сориентироваться в первые дни работы '
                'и узнать больше о нашей компании. '
                'Посещаете ли вы офис в Москве?')
    elif query.data == 'old_employee':
        text = ('Здорово, что вы присоединились к чат-боту! '
                'Он поможет вам структурировать  информацию '
                'о нашей компании воедино или узнать что-то новое. '
                'Вы сможете задать свои вопросы и озвучить '
                'предложения по улучшению. '
                'Посещаете ли вы офис в Москве?')

    keyboard = [
        [
            InlineKeyboardButton('Да', callback_data='moscow_yes'),
            InlineKeyboardButton('Нет', callback_data='moscow_no'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=text, reply_markup=reply_markup)


def info_buttons(update, context):
    """Обработчик нажатия кнопок"""
    query = update.callback_query
    query.answer()

    if query.data == 'moscow_yes':
        keyboard = [
            [  # на будущее - тут можно подгружать кнопки из базы
                InlineKeyboardButton(
                    'Кнопка посещающих Москву',
                    callback_data='moscow_button')
            ]
        ]
    elif query.data == 'moscow_no':
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

    # Обработчик команды /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Обработчик для кнопок выбора нового или старого сотрудника.
    # Pattern нужен чтобы Обработчик реагировал только на определённые запросы
    dispatcher.add_handler(CallbackQueryHandler(
        moscow_office,
        pattern='^(new_employee|old_employee)$'))

    # Обработчик для кнопок ответа о посещении офиса в Москве
    dispatcher.add_handler(
        CallbackQueryHandler(info_buttons, pattern='^(moscow_yes|moscow_no)$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
