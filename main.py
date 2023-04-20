from os import getenv

import requests
from flask import Flask
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

telegram_bot_token = getenv('TELEGRAM_BOT_TOKEN')

app = Flask(__name__)

app.config.from_prefixed_env() # FLASK_ prefix for env variables

@app.route('/hello')
def hello_geek():
    """Adds two numbers together and returns the result."""
    return "<h1>Hello from Flask & Docker</h2>"

@app.route('/')
def get_info(word):
    """Get word info - request from api and returns the response data"""
    logging.info("get_info provoked - api request sent")
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(word)
    logging.info(f"word is {word}")

    response = requests.get(url)

    # return a custom response if an invalid word is provided
    if response.status_code == 404:
        error_response = 'We are not able to provide any information about your word. Please confirm that the word is '\
                         'spelled correctly or try the search again at a later time.'
        return error_response

    data = response.json()[0]
    return data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot. """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me Atara!!!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echos the message received."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Caps the message received.(returns as upper case)"""
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


if __name__ == "__main__":

    application = ApplicationBuilder().token(telegram_bot_token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    from dictionaryApi import start_dic
    start_dictionary = CommandHandler('dic', start_dic)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(start_dictionary)

    application.run_polling()
    app.run(debug=True)
