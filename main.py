
from os import getenv
from flask import Flask
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from chatGPTHandler import start_chatgpt, chatgpt_message_handler
from zipHandler import file_paths, zip_command, endzip_command
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
    """File handler for documents/voice message received. """
    logging.info("File handler provoked.")
    if update.message.voice is not None:
        logging.info(f"Voice message received.")
        await audio_handler(update, context)
    elif update.message.document:
        logging.info(f"Document received.")
        document = update.message.document
        file_path = f"/data/{document.file_name}"
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(file_path)
        logging.info(f"Document saved in path {file_path}.")
        file_paths.append(file_path)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="File saved successfully.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm not here to handle that kind of file.")


if __name__ == "__main__":

    application = ApplicationBuilder().token(telegram_bot_token).build()

    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    from dictionaryApi import start_dic
    start_dictionary = CommandHandler('dic', start_dic)
    voice_message_handler = MessageHandler(filters.AUDIO & ~filters.COMMAND, audio_handler)
    file_handler = MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, file_handler)
    chatgpt_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chatgpt_message_handler)

    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(start_dictionary)
    application.add_handler(voice_message_handler)
    application.add_handler(file_handler)
    application.add_handler(chatgpt_message_handler)
    application.add_handler(CommandHandler("zip", zip_command))
    application.add_handler(CommandHandler("endzip", endzip_command))
    application.add_handler(CommandHandler('chatgpt', start_chatgpt))
    # application.add_handler(echo_handler)

    application.run_polling()
    app.run(debug=True)
