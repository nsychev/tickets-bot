#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
import re
from config import TOKEN, URL

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

RE = re.compile(r'\d+')
TICKETS = open("../data/ticketnames.txt", "r").read().split("\n")

def start(bot, update):
    update.message.reply_text('''Привет! Я расскажу тебе о билетах по матану в красивых картинках. Спроси меня любой билет и я тебе отправлю картинку

[Бота](https://github.com/nsychev/tickets-bot) сделал @nsychev · Билеты написал @cannor147''', parse_mode="Markdown", disable_web_page_preview=True)

def ticket(bot, update):
    if not update.message:
        return
    text = update.message.text
    result = re.search(RE, text)
    if result is None:
        update.message.reply_text("Не нашел число в твоём сообщении :(")
        return
    
    num = int(result.group(0)) - 1
    if num >= len(TICKETS) or num < 0:
        update.message.reply_text("Билеты имеют номера с 1 до {}. Попробуй другое число".format(len(TICKETS)))
        return
    
    ticket_name = TICKETS[num]
    update.message.reply_photo(
        URL.format(num),
        caption=ticket_name
    )
    
def TrueFilter(*args, **kwargs):
    return True

def error(bot, update, error):
    logger.warning(str(error))

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", start))
dp.add_handler(MessageHandler(TrueFilter, ticket))
dp.add_error_handler(error)

updater.start_polling()
updater.idle()
