import asyncio
import importlib
from unittest.mock import MagicMock, patch

from telegram import Update
from telegram.ext import ContextTypes
from ..dictionaryApi import get_info, start_dic, get_word_info

class MagicAsyncMock(MagicMock):
    def __await__(self):
        fut = asyncio.Future()
        fut.set_result(self)
        return fut.__await__()

def test_get_word_info():
    # Mock the necessary objects
    update = MagicMock(spec=Update)
    context = MagicMock()
    context.args = ['test']

    # Mock the reply_text method
    update.message.reply_text = MagicAsyncMock()

    # Run the async function synchronously within an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_word_info(update, context))

    # Assert the expected behavior
    update.message.reply_text.assert_called_with('We are not able to provide any information about your word. Please confirm that the word is spelled correctly or try the search again at a later time.')


def test_get_info():
    # Mock the necessary objects
    word = 'test'
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/test'
    response_data = {'word': 'test', 'meanings': [{'definitions': [{'definition': 'This is a test.'}]}]}

    # Mock the requests.get method
    requests_get_mock = MagicMock()
    requests_get_mock.return_value = MagicMock()
    requests_get_mock.return_value.status_code = 200
    requests_get_mock.return_value.json.return_value = [response_data]

    # Patch the requests.get method
    with patch('requests.get', requests_get_mock):
        # Call the function
        result = get_info(word)

    # Assert the expected behavior
    assert result == response_data

    # Assert that requests.get was called with the correct URL
    requests_get_mock.assert_called_with(url)

# def test_start_dic():
#     # Mock the necessary objects
#     update = MagicMock(spec=Update)
#     context = MagicMock()
#     context.args = ['test']
#
#     # Mock the get_word_info function
#     get_word_info_mock = MagicMock()
#     get_word_info_mock.return_value = MagicAsyncMock()
#
#     # Get the target function dynamically
#     package_name = __package__.rsplit('.', 1)[0]
#     module_name = f'{package_name}.dictionaryApi'
#     module = importlib.import_module(module_name)
#     get_word_info_func = getattr(module, 'get_word_info')
#
#     get_word_info_mock.__name__ = 'get_word_info'
#     # Patch the get_word_info function
#     with patch.object(get_word_info_func, '__name__', return_value='get_word_info'):
#         with patch.object(module, 'get_word_info', get_word_info_mock):
#             # Perform your test assertions
#             pass