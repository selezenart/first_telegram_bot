import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)
text_message1 = "Man I wanna play some chess!"
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
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("It sucks...", callback_data="suck")
            item2 = types.InlineKeyboardButton("Fuck you!", callback_data="fuck")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "I don't have that mode yet, dumbass", reply_markup=markup)

        elif message.text == text_message2:
            bot.send_message(message.chat.id, "I AM NOT WATCHING ANIME, I HAVE JUST SEEN A COUPLE OF COMPILATIONS!!")
        else:
            bot.send_message(message.chat.id, "Man I have no words")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "suck":
                bot.send_message(call.message.chat.id, "Just wait a bit, OK?")
            if call.data == "fuck":
                bot.send_message(call.message.chat.id, "No, fuck you")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text_message1,
                                  reply_markup=None)
    #           bot.answer_callback_query(callback_query_id=call.message.chat.id,show_alert=True,text="SURPRISEMOTHAFAKA!")

    except Exception as e:
        print(repr(e))


# Run
bot.polling(none_stop=True)
