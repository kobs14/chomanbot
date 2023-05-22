from unittest.mock import MagicMock
from telegram import Update, Message, Document
from telegram.ext import ContextTypes
from ..main import file_handler
import asyncio

class MagicAsyncMock(MagicMock):
    def __await__(self):
        fut = asyncio.Future()
        fut.set_result(self)
        return fut.__await__()

def test_file_handler():
    # Create an event loop
    loop = asyncio.get_event_loop()

    # Mock the necessary objects using MagicAsyncMock
    update = MagicAsyncMock(spec=Update)
    context = MagicAsyncMock()
    message = MagicAsyncMock(spec=Message)
    document = MagicAsyncMock(spec=Document)

    # Set the necessary attributes and return values
    update.message = message
    update.effective_chat.id = 12345
    update.message.voice = None
    update.message.document = document
    document.file_id = 'file_id'
    document.file_name = 'file_name'

    # Mock the required methods
    file_mock = MagicAsyncMock(download_to_drive=MagicAsyncMock())
    context.bot.get_file.return_value = file_mock

    # Run the async function synchronously
    loop.run_until_complete(file_handler(update, context))

    # Assert the expected behavior
    context.bot.send_message.assert_called_with(chat_id=12345, text="File saved successfully.")
    context.bot.get_file.assert_called_with('file_id')
    file_mock.download_to_drive.assert_called_with('/data/file_name')


