import requests
from telegram import Update
from telegram.ext import ContextTypes


def get_info(word):
    """Get word info - request from api and returns the response data"""
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(word)

    response = requests.get(url)

    # return a custom response if an invalid word is provided
    if response.status_code == 404:
        error_response = 'We are not able to provide any information about your word. Please confirm that the word is '\
                         'spelled correctly or try the search again at a later time.'
        return error_response

    data = response.json()[0]
    return data

# set up the introductory statement for the bot when the /start command is invoked
async def start_dic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts dictionary"""
    chat_id = update.effective_chat.id
    # await context.bot.send_message(chat_id=chat_id, text="Hello there. Provide any English word and I will give you a bunch "
    #                                                "of information about it.")
    await get_word_info(update, ' '.join(context.args))


# obtain the information of the word provided and format before presenting.
async def get_word_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get word info - request from api and returns the response data"""
    # get the word info
    word_info = get_info(context)

    # If the user provides an invalid English word, return the custom response from get_info() and exit the function
    if word_info.__class__ is str:
        await update.message.reply_text(word_info)
        return

    # get the word the user provided
    word = word_info['word']

    meanings = '\n'

    synonyms = ''
    definition = ''
    example = ''
    antonyms = ''

    # a word may have several meanings. We'll use this counter to track each of the meanings provided from the response
    meaning_counter = 1

    for word_meaning in word_info['meanings']:
        meanings += 'Meaning ' + str(meaning_counter) + ':\n'

        for word_definition in word_meaning['definitions']:
            # extract each of the definitions of the word
            definition = word_definition['definition']

            # extract each example for the respective definition
            if 'example' in word_definition:
                example = word_definition['example']

            # extract the collection of synonyms for the word based on the definition
            for word_synonym in word_definition['synonyms']:
                synonyms += word_synonym + ', '

            # extract the antonyms of the word based on the definition
            for word_antonym in word_definition['antonyms']:
                antonyms += word_antonym + ', '

        meanings += 'Definition: ' + definition + '\n\n'
        meanings += 'Example: ' + example + '\n\n'
        meanings += 'Synonym: ' + synonyms + '\n\n'
        meanings += 'Antonym: ' + antonyms + '\n\n\n'

        meaning_counter += 1

    # format the data into a string
    message = f"Word: {word}\n\n {meanings}"

    await update.message.reply_text(message)