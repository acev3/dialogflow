import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import random
import logging

logger = logging.getLogger(__file__)


def send_message(event, vk_api, dialogflow_answer):
    vk_api.messages.send(
        user_id=event.user_id,
        message=dialogflow_answer,
        random_id=random.randint(1,1000)
    )


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
    if response.query_result.intent.is_fallback:
        return False
    return response.query_result.fulfillment_text


def main():
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    load_dotenv()
    vk_token = os.environ["VK_GROUP_API_TOKEN"]
    project_id = os.environ["PROJECT_ID"]
    vk_session = vk.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            logger.info("Новое сообщение:")
            if event.to_me:
                dialogflow_answer = detect_intent_texts(project_id, event.user_id, [event.text], language_code="ru")
                if dialogflow_answer:
                    send_message(event, vk_api, dialogflow_answer)
                    logger.info("Для меня от: {}".format(event.user_id))
            else:
                logger.info("От меня для: {}".format(event.user_id))
            logger.info("Текст: {}".format(event.text))


if __name__ == '__main__':
    main()