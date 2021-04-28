from dotenv import load_dotenv
import os
import json


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    project_id = os.environ["PROJECT_ID"]
    with open("questions.json", "r") as my_file:
        questions = json.load(my_file)
    for question in questions.keys():
        questions[question]
        display_name = question
        training_phrases_parts = questions[question]["questions"]
        message_texts = [questions[question]["answer"]]
        create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
     main()