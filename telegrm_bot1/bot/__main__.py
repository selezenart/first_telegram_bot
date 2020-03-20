# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)
text_message1 = "Man I wanna play some chess!"
text_message2 = "What's up?"


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Hello there! You are {0.first_name} {0.last_name}, aren't you?!\nI've been "
                                      "waiting for you. Now, apparently I am still developed by "
                                      "some lazyass bastard, but soon I'll be powerful enough to entertain you! Type "
                                      "/help to see what options are ready.".
                     format(message.from_user, bot.get_me(), parse_mode='html'))


@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.chat.id, "So, now you only can /start me, start a small talk typing /talk, start playing "
                                      "/chess. That's all, "
                                      "folks! ".format(message.from_user), parse_mode='html')


@bot.message_handler(commands=['chess'])
def chess(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("It sucks...", callback_data="suck")
    item2 = types.InlineKeyboardButton("Fuck you!", callback_data="fuck")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "I don't have that mode yet, dumbass", reply_markup=markup)


@bot.message_handler(commands=['talk'])
def talk(message):
    if message.chat.first_name == "Artem" or message.chat.first_name == "Artyom" or message.chat.first_name == u"Артем" \
            or message.chat.first_name == u"Артём":
        bot.send_message(message.chat.id, "Man i don't wanna talk to you! I'm glad to talk only with a human but not "
                                          "with {0.first_name}".format(message.from_user), parse_mode="html")
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Sad...", callback_data="sad")
        item2 = types.InlineKeyboardButton("Good, and you?", callback_data="good")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "So, {0.first_name}, how are you?".format(message.from_user),
                         reply_markup=markup, parse_mode="html")


@bot.message_handler(content_types=['text'])
def reply(message):
    if message.chat.type == "private":
        if message.text == "What's up?":
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
            if call.data == "sad":
                bot.send_message(call.message.chat.id, "Well, shit happens")
            if call.data == "good":
                bot.send_message(call.message.chat.id, "I am soulless robot. How do you think I can feel?")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="I don't have"
                                                                                                         "that mode "
                                                                                                         "yet, "
                                                                                                         "dumbass" or
                                                                                                         "So, "
                                                                                                         "how are "
                                                                                                         "you?",
                                  reply_markup=None)
    #           bot.answer_callback_query(callback_query_id=call.message.chat.id,show_alert=True,text="SURPRISEMOTHAFAKA!")

    except Exception as e:
        print(repr(e))


# Run
bot.polling(none_stop=True)
