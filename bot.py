from telegram.ext import Updater, CommandHandler
import logging
from logic import *
from stickbug import *
import os
import numpy as np


def start(update, context):
    if (update.effective_user.username == 'vim_miv'):
        message = "Oi Vim, te amo <3"
    else: 
        message = "Oi, @{}! Digite /help para ver os comandos \o/.".format(update.effective_user.username)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def help(update, context):
    message = """
    Comandos: 

    /help: Mostra comandos
    /tabela: Faz a tabela verdade de uma expressão
    /expressao: Faz a expressão de uma tabela 
    /getstickbugged: Use o comando respondendo à um vídeo
    """    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Gets you stick bugged
def getstickbugged(update, context):
    media = update.message.reply_to_message.video
    if (media == None): return
    if (media.file_size > 15619356): return
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="To carregando, pera...")

    media_id = media.file_id
    media_type = f"{media.mime_type}".split('/')[-1]
    videoFile = context.bot.getFile(media_id)

    fname = f'{media_id}.{media_type}'
    videoFile.download(fname)
    stickbug(fname)
    os.remove(fname)
    context.bot.sendVideo(chat_id=update.effective_chat.id, video=open(f"out-{fname}", 'rb'))
    os.remove(f"out-{fname}")


# Faz a tabela verdade a partir de uma expressão
def tabela(update, context):
    expr = context.args
    expr = ' '.join(expr)
    message = tableFromExpression(expr)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Encontra a expressão por traz de uma tabela verdade
def expressao(update, context):
    table = [list(p) for p in context.args]
    message = expessionFromTable(table)
    message = str(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")


    TOKEN = os.environ['API_KEY']
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tabela", tabela))
    dp.add_handler(CommandHandler("expressao", expressao))
    dp.add_handler(CommandHandler("getstickbugged", getstickbugged))

    updater.start_polling()
    logging.info("=== It's alive! ===")
    updater.idle()
    logging.info("=== Oh no, It's dying! ===")


if __name__ == "__main__":
    main()