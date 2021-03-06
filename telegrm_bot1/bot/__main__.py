# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config

from game.chess.gamestate import GameState
from game.chess.models import Board

bot = telebot.TeleBot(config.TOKEN)

new_board: Board
game_state: GameState
previous_message = None


def refresh_board(call, board_x, board_y):
    new_board.move(game_state.holding_chessman, board_x, board_y)
    game_state.leave_chessman()
    game_state.change_turn()
    bot.edit_message_text("Turn " + game_state.turn.value, call.message.chat.id, call.message.message_id)
    new_board.redraw()
    markup = types.InlineKeyboardMarkup(row_width=8)
    for y in range(8):
        markup.add(
            *[types.InlineKeyboardButton(str(new_board.board[x][y]),
                                         callback_data=new_board.board[x][y].CALLBACK) for x in range(8)])
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=markup)


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


@bot.message_handler(commands=['init'])
def send_board(message):
    global previous_message, game_state, new_board
    if previous_message is not None:
        bot.delete_message(chat_id=previous_message.chat.id, message_id=previous_message.message_id + 1)
        bot.delete_message(chat_id=previous_message.chat.id, message_id=previous_message.message_id)
    previous_message = message
    new_board = Board()
    game_state = GameState(message, new_board)
    markup = types.InlineKeyboardMarkup(row_width=8)
    for y in range(8):
        markup.add(
            *[types.InlineKeyboardButton(str(new_board.board[x][y]), callback_data=new_board.board[x][y].CALLBACK) for x
              in range(8)])
    bot.send_message(message.chat.id, "Turn " + game_state.turn.value, reply_markup=markup)


@bot.message_handler(commands=['chess'])
def chess(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
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
        markup = types.InlineKeyboardMarkup(row_width=1)
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
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="I don't have that mode yet, dumbass",
                                      reply_markup=None)
            elif call.data == "fuck":
                bot.send_message(call.message.chat.id, "No, fuck you")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="I don't have that mode yet, dumbass",
                                      reply_markup=None)
            elif call.data == "sad":
                bot.send_message(call.message.chat.id, "Well, shit happens")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="So, {0.first_name}, how are you?",
                                      reply_markup=None)
            elif call.data == "good":
                bot.send_message(call.message.chat.id, "I am soulless robot. How do you think I can feel?")

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="So, {0.first_name}, how are you?",
                                      reply_markup=None)
            elif call.data.partition('pawn')[1] == "pawn":
                attacked = new_board.get_chessman_call(call)
                if game_state.holding_chessman is not None:
                    if game_state.allow_attack(call, attacked.X, attacked.Y):
                        refresh_board(call, attacked.X, attacked.Y)
                    else:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                  text="Invalid move!")
                else:
                    if game_state.allow_turn(call):
                        game_state.capture_chessman(new_board.get_chessman_call(call))
                    else:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                  text="You cannot choose that chessman!")
            elif call.data.partition('king')[1] == 'king':
                attacked = new_board.get_chessman_call(call)
                if game_state.holding_chessman is not None:
                    if game_state.allow_attack(call, attacked.X, attacked.Y):
                        refresh_board(call, attacked.X, attacked.Y)
                    else:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                  text="This cell is already taken!")
                else:
                    if game_state.allow_turn(call):
                        game_state.capture_chessman(new_board.get_chessman_call(call))
                    else:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                  text="You cannot choose that chessman!")
            elif call.data.partition('empty')[1] == "empty":
                if game_state.holding_chessman is not None:
                    if game_state.allow_move(call.data.split(' ')[1], call.data.split(' ')[2],
                                             game_state.holding_chessman):
                        refresh_board(call, call.data.split(' ')[1], call.data.split(' ')[2])
                    else:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                  text="Invalid move!")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="You did'nt choose a chessman!")
            else:
                bot.send_message(call.message.chat.id, call.data)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="I don't have"
                                           "that mode "
                                           "yet, "
                                           "dumbass" or
                                           "So, "
                                           "how are "
                                           "you?" or "test",
                                      reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
