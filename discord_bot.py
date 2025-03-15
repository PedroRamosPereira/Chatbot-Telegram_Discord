import discord
from ai import responder, limpar_historico
import json

with open('token.json') as token_file:
    token = json.load(token_file)

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content == "!limpar":
            await message.channel.send(limpar_historico('tester1'))
        else:
            resposta = responder("tester1", "discord", message.content)
            await message.channel.send(resposta)

client = MyClient()
client.run(token['bot_discord'])