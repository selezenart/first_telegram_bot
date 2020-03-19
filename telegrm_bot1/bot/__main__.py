import telebot
import config


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def repeater(messege):
    bot.send_message(messege.chat.id, messege.text)


#Run
bot.polling(none_stop=True)