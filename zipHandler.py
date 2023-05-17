import logging
from telegram import InputFile
import os
import zipfile
from pathlib import Path

# Global variable to store file paths
file_paths = []

async def zip_files(update, context):
    """Zip handler for documents received. """
    logging.info("File handler provoked.")
    if not file_paths:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No files to zip.")
        return
    try:
        zip_path = "/data/files.zip"
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for file_path in file_paths:
                zip_file.write(file_path, os.path.basename(file_path))
        logging.info("Files zipped.")
        await context.bot.send_document(chat_id=update.effective_chat.id,
                                        document=InputFile(zip_path, filename='files.zip'))
        logging.info("Document sent to user- files.zip")
    finally:
        zip_path_to_delete = Path(zip_path)
        # Delete zip file
        zip_path_to_delete.unlink()  # delete the zip file
        # Delete saved files
        for file_path in file_paths:
            # os.remove(file_path)
            Path(file_path).unlink()
        # Clear the file_paths list
        file_paths.clear()

async def zip_command(update, context):
    """Zip command. """
    logging.info("Zip command provoked.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send the files you want to include in the zip.")

async def endzip_command(update, context):
    """End-Zip command zip documents saved by user then sends back the zip file. """
    logging.info("End-Zip provoked.")
    await zip_files(update, context)