from os import getenv
import openai
import uuid
import logging

openai.api_key  = getenv("OPENAI_API_KEY")

async def start_chatgpt(update, context):
    """Zip handler for documents received. """
    logging.info("start_chatgpt provoked.")
    # Start the chat with ChatGPT and store the conversation ID in the user's context
    conversation_id = str(uuid.uuid4())
    context.user_data["chatgpt_conversation_id"] = conversation_id
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You are now chatting with ChatGPT!")

async def chatgpt_message_handler(update, context):
    """Zip handler for documents received. """
    logging.info("chatgpt_message_handler provoked.")
    # Get the user's message
    message = update.message.text

    # Retrieve the conversation ID from the user's context
    conversation_id = context.user_data.get("chatgpt_conversation_id")

    # Send the user's message to ChatGPT and get the response
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        conversation_id=conversation_id,
    )

    # Extract the generated reply from the response
    reply = response.choices[0].text.strip()

    # Send the reply back to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

