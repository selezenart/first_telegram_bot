import telebot
import config


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(messege):
    bot.send_message(messege.chat.id, "Hello there! You are {0.first_name} {0.last_name}, aren't you?!\nI've been "
                                      "waiting for you. Now, apparently I am still developed by "
                                      "some lazyass bastard, but soon I'll be powerful enough to entertain you!".format(messege.from_user, bot.get_me(), parse_mode='html'))


@bot.message_handler(content_types=['text'])
def repeater(messege):
    bot.send_message(messege.chat.id, messege.text)


#Run
bot.polling(none_stop=True)
