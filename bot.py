from telegram.ext import Updater, CommandHandler
import logging
from logic import *
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
    /expressao: Faz a expressão de uma tabela verdade
    """    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

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

    updater.start_polling()
    logging.info("=== It's alive! ===")
    updater.idle()
    logging.info("=== Oh no, It's dying! ===")


if __name__ == "__main__":
    main()