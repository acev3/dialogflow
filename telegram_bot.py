from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__file__)


def start(bot, update):
    chat_id = os.environ['CHAT_ID']
    bot.sendMessage(chat_id=chat_id, text="Здравствуйте")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def send_message(bot, update):
    chat_id = os.environ['CHAT_ID']
    project_id = os.environ['PROJECT_ID']
    dialogflow_answer = detect_intent_texts(project_id, chat_id ,[update.message.text], language_code="ru")
    bot.sendMessage(chat_id=chat_id, text=dialogflow_answer)


def detect_intent_texts(project_id, session_id, texts, language_code="ru-RU"):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    logger.info("Session path: {}\n".format(session))
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        logger.info("=" * 20)
        logger.info("Query text: {}".format(response.query_result.query_text))
        logger.info(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        logger.info("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


def main():
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    chat_id = os.environ['CHAT_ID']
    api_tme_token = os.environ["TELEGRAM_API_TOKEN"]
    updater = Updater(token=api_tme_token)
    start_handler = CommandHandler("start", start)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, send_message))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()

if __name__ == '__main__':
     main()