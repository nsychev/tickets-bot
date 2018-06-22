#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import InputMediaPhoto
import logging, re, os, yaml, traceback

from threading import Thread
from time import sleep

from models import *
from config import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

RE = re.compile(r"\d+")
BLACKLIST = []


def scan(bot, update):
    if update.message.chat.id != ADMIN_ID:
        return
    
    bot.send_chat_action(update.message.chat.id, "typing")
    
    try:
        db.drop_tables([Ticket, Image])
        
        db.create_tables([Ticket, Image])
        
        for dir in os.listdir(PATH):
            if not os.path.isdir(os.path.join(PATH, dir)) or dir.startswith("."):
                continue
            
            config = yaml.load(open(os.path.join(PATH, dir, "config.yml")).read())
            ticket = Ticket.create(id=dir, name=config["name"], tag=config["tag"])
            
            for file in sorted(os.listdir(os.path.join(PATH, dir))):
                if file.endswith(".yml"):
                    continue
                image = Image.create(
                    ticket=ticket,
                    filename=file
                )
    except Exception as e:
        update.message.reply_text("\u274c **Failed**:\n```" + traceback.format_exc() + "```", parse_mode="Markdown")
        return
    
    update.message.reply_text("\u2705 **Success**: update tickets", parse_mode="Markdown")


def start(bot, update):
    update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown", disable_web_page_preview=True)

    
def help(bot, update):
    update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")


def ticket(bot, update):
    if not update.message:
        return
    text = update.message.text
    result = re.search(RE, text)
    if result is None:
        return search(bot, update)
    
    num = int(result.group(0))
    try:
        ticket = Ticket.get(Ticket.id == num)
    except Ticket.DoesNotExist:
        update.message.reply_text("Не могу найти билет #{}\n\n/help — справка".format(num))
    
    update.message.reply_text(ticket.name)
    
    for photo in ticket.image_set.order_by(Image.filename):        
        if photo.file_id:
            bot.send_photo(update.message.chat.id, photo.file_id)
        else:
            bot.send_chat_action(update.message.chat.id, "upload_photo")
            with open(os.path.join(PATH, str(num), photo.filename), "rb") as f: 
                message = bot.send_photo(update.message.chat.id, f)
            photo.file_id = message.photo[-1].file_id
            photo.save()

     
def search(bot, update):
    response = ""
    query = update.message.text.replace(" ", "|")
    try:
        for ticket in Ticket.select().where(Match(Ticket.name, query)):
            response += "/{} {}\n".format(ticket.id, ticket.name)
    except:
        pass
    if response == "":
        response = "Ничего не найдено"
    update.message.reply_text(response)
     
def dump_thread(bot, update):
    update.message.reply_text("Никто тебя не просил это делать! Ты сам захотел!\n\nДанный процесс займет продолжительное время, т.к. я не хочу проблем с лимитами Телеграма")
    bot.send_chat_action(update.message.chat.id, "upload_photo")
    sleep(1)
    try:
        for photo in Image.select():
            sleep(1)
            if photo.file_id:
                bot.send_photo(update.message.chat.id, photo.file_id)
            else:
                bot.send_chat_action(update.message.chat.id, "upload_photo")
                with open(os.path.join(PATH, str(photo.ticket.id), photo.filename), "rb") as f: 
                    message = bot.send_photo(update.message.chat.id, f)
                photo.file_id = message.photo[-1].file_id
                photo.save()
    except:
        update.message.reply_text("\u274c **Failed**:\n```" + traceback.format_exc() + "```", parse_mode="Markdown")

            
def dump(bot, update):
    if update.message.chat.id in BLACKLIST:
        update.message.reply_text("Данная функция недоступна для вашего аккаунта")
        return
    BLACKLIST.append(update.message.chat.id)
    thread = Thread(target = dump_thread, args=(bot, update))
    thread.start()
    

def TagFactory(tag):
    def process_tag(bot, update):
        response = ""
        for ticket in Ticket.select().where(Ticket.tag == tag).order_by(Ticket.id):
            response += "/{} {}\n".format(ticket.id, ticket.name)
        update.message.reply_text(response)
    return process_tag


def TrueFilter(*args, **kwargs):
    return True


def error(bot, update, error):
    logger.warning(str(error))

    
if __name__ == "__main__":    
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("scan", scan))
    dp.add_handler(CommandHandler("min", TagFactory("min")))
    dp.add_handler(CommandHandler("mod3", TagFactory("mod3")))
    dp.add_handler(CommandHandler("mod4", TagFactory("mod4")))
    dp.add_handler(CommandHandler("dump_all", dump))
    dp.add_handler(MessageHandler(TrueFilter, ticket))
    dp.add_error_handler(error)
    
    logger.info("Waiting postgres")
    sleep(5.0)
    logger.info("Starting...")
    db.connect()

    updater.start_polling()
    updater.idle()
