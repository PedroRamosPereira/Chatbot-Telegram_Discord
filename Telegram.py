from ai import responder, limpar_historico
import telebot
import json

with open('token.json') as token_file:
    token = json.load(token_file)

bot = telebot.TeleBot(token['bot_telegram'])

commands = ['limpar']

def verificar(message):
    for x in commands:
        comando = '/'+ x 
        if(message.text != comando):
            return(True)
        
@bot.message_handler(func=verificar)
def reponder(message):
    resposta = responder("tester1", "telegram", message.text)
    bot.reply_to(message, resposta)

@bot.message_handler(commands = commands)
def limpar(message):
    bot.reply_to(message, limpar_historico("pedro"))

bot.polling()