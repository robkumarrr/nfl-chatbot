""" This program is used in conjunction with ai_bot_discord.py to provide functionality
for an OpenAI API-driven bot. The bot has been constructed to work with a set of questions that
have been engineered to retrieve answers as if the bot were an NFL analyst.

Robert Kumar & Rodrigo Wong Mac
March 15, 2024
"""
from openai import OpenAI
# import list of dictionaries for classification and responses
from openai_examples import example_classification_prompts, example_response_prompts
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def classify_utterance(utterance):
    """Classify the utterance using a chat model."""
    engineered_classification_prompts = example_classification_prompts
    engineered_classification_prompts.append({"role": "user", "content": utterance})
    classification_criteria = engineered_classification_prompts
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=classification_criteria,
        temperature=0.2,
        max_tokens=100
    )
    classification = response.choices[0].message.content
    return classification


def openai_api_call(utterance, classification, conversation_history):
    """Generate a response using the OpenAI API, based on the classification of the utterance."""
    engineered_response_prompt = example_response_prompts
    # Construct the prompt based on the classification
    engineered_prompt = f"Classification: {classification} Utterance: {utterance}"
    engineered_response_prompt.append({"role": "user", "content": engineered_prompt})

    # Construct the dialog for the API call
    dialog = engineered_response_prompt
    for interaction in conversation_history[-5:]:  # Keep the last 5 interactions
        dialog.append({"role": "user", "content": interaction["user"]})
        dialog.append({"role": "assistant", "content": interaction["bot"]})

    # Make the API call with a higher temperature for more variability
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=dialog,
        temperature=0.7,  # Increase the temperature for more diverse responses
        max_tokens=256
    ).choices[0].message.content

    return response


def main():
    print("Bot: Hello! I'm a football analyst chat bot! Let's chat!")
    print()
    conversation_history = []
    while True:
        utterance = input("User: ")
        if utterance.lower() == "goodbye":
            break
        classification = classify_utterance(utterance)
        # Append the current utterance to the conversation history before the API call
        conversation_history.append({"user": utterance, "bot": "", "classification": classification})
        if len(conversation_history) > 5:
            conversation_history.pop(0)  # Remove the oldest interaction to keep the history size at 5
        response = openai_api_call(utterance, classification, conversation_history)
        # Update the bot's response in the conversation history after the API call
        conversation_history[-1]["bot"] = response
        print("Bot:", response)
        print()

    print("Nice talking to you!")


if __name__ == "__main__":
    main()
