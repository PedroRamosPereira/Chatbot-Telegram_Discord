import discord
import telebot
import asyncio
import json
from ai import responder, limpar_historico 

with open('token.json') as token_file:
    token = json.load(token_file)

# Discord

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
            await message.channel.send(limpar_historico(token['nome']))
        else:
            resposta = responder(token['nome'], "discord", message.content)
            await message.channel.send(resposta)

# Telegram

bot = telebot.TeleBot(token['bot_telegram'])

commands = ['limpar']

def verificar(message):
    for x in commands:
        comando = '/' + x 
        if(message.text != comando):
            return(True)

@bot.message_handler(func=verificar)
def reponder(message):
    resposta = responder(token['nome'], "telegram", message.text)
    bot.reply_to(message, resposta)

@bot.message_handler(commands=commands)
def limpar(message):
    bot.reply_to(message, limpar_historico(token['nome']))

#executar os bots

async def run_bots():
    loop = asyncio.get_event_loop()

    discord_bot = MyClient()
    discord_task = loop.create_task(discord_bot.start(token['bot_discord']))

    telegram_task = loop.run_in_executor(None, bot.polling)

    await discord_task
    await telegram_task

if __name__ == "__main__":
    asyncio.run(run_bots())