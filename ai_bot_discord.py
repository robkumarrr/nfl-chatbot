""" This program launches a discord bot using its associated bot_token.
The bot implements the assignment_4_faq_bot.py program, which loads in a
series of questions and answers regarding the NFL. The bot uses the OpenAI
API to craft intelligent responses to various queries.

Rob Kumar & Rodrigo Wong Mac
March 15, 2024
"""
import discord
from ai_bot import classify_utterance, openai_api_call
import os

class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        self.conversation_history = []  # Initialize conversation history as an instance variable
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        # Checks if we @ mentioned the bot in the chat
        if not self.user.mentioned_in(message):
            return

        # get the utterance and generate the response
        utterance = message.content
        classification = classify_utterance(utterance)
        # Append the current utterance to the conversation history before the API call
        self.conversation_history.append({"user": utterance, "bot": "", "classification": classification})
        if len(self.conversation_history) > 5:
            self.conversation_history.pop(0)  # Remove the oldest interaction to keep the history size at 5
        response = openai_api_call(utterance, classification, self.conversation_history)
        # Update the bot's response in the conversation history after the API call
        self.conversation_history[-1]["bot"] = response
        # send the response
        await message.channel.send(response)


# Set up and log in
client = MyClient()
client.run(os.getenv('DISCORD_BOT_TOKEN'))
