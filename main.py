import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6467041432:AAH_FdrhN6Wm8pcQtzYwC7V25_FJvTJpn-g",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    mem = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Знакомство"
text_button_1 = "О себе"
text_button_2 = "Расслабься"
text_button_3 = "Кнопка 3"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Это мой бот.Надеюсь вам понравится!',
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Давай познакомимся!Как тебя зовут?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'А меня Лёня.Спроси у меня что нибудь')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Боюсь я не смогу ответить тебе, давай ещё раз. ', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=PollState.mem)
def mem(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['mem'] = message.text
    bot.send_message(message.chat.id, *'Ты задаёшь очень сложные вопросы.Попробуй другие функции. ', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)




@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, " Меня зовут Лёня.Я учусь в Химкинской школе №8.Хочу связать свою жизнь с IT и стать членом вашей команды.Также я проходил курсы по питону и подготовку к ОГЭ по информатике на УМСКУЛ.", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Я так расслабляюсь!](https://www.youtube.com/watch?v=Nj6aM9ljdQU)", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Могу показать котиков!](https://www.youtube.com/watch?v=-452p_9ESbM) Надеюсь тебе понравится", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
