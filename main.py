
from os import getenv
from flask import Flask
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from voiceChanger import audio_handler

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot. """
    logging.info("Start provoked.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me Atara!!!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echos the message received."""
    logging.info("echo provoked.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Caps the message received.(returns as upper case)"""
    logging.info("caps provoked.")
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Audio handler for voice messages received. """
    logging.info("File handler provoked.")
    if update.message.voice is not None:
        logging.info(f"voice message received.")
        await audio_handler(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="What a nice sound! I'm not here to listen to some audio, tho. My work is to wish a good night to all members of a group chat")


if __name__ == "__main__":

    application = ApplicationBuilder().token(telegram_bot_token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    voice_message_handler = MessageHandler(filters.AUDIO & ~filters.COMMAND, audio_handler)
    file_handler = MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, file_handler )
    caps_handler = CommandHandler('caps', caps)
    from dictionaryApi import start_dic
    start_dictionary = CommandHandler('dic', start_dic)
    application.add_handler(voice_message_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(start_dictionary)
    application.add_handler(file_handler)


    application.run_polling()
    app.run(debug=True)
