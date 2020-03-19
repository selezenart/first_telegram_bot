import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)
text_message1 ="Man I wanna play some chess!"
text_message2 = "Wat's up?"


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text_message1)
    item2 = types.KeyboardButton(text_message2)

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Hello there! You are {0.first_name} {0.last_name}, aren't you?!\nI've been "
                                      "waiting for you. Now, apparently I am still developed by "
                                      "some lazyass bastard, but soon I'll be powerful enough to entertain you!".
                     format(message.from_user, bot.get_me(), parse_mode='html'), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def reply(message):
    if message.chat.type == "private":
        if message.text == text_message1:
            bot.send_message(message.chat.id,"I don't have that mode yet, dumbass")
        elif message.text == text_message2:
            bot.send_message(message.chat.id,"I AM NOT WATCHING ANIME, I HAVE JUST SEEN A COUPLE OF COMPILATIONS!!")
        else:
            bot.send_message(message.chat.id,"Man I have no words")


# Run
bot.polling(none_stop=True)
