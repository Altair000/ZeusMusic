import telebot
import os
from bot.handlers import bot
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = os.getenv('Token')
HEROKU_URL = 'https://zeusmusicbot-610073f53b03.herokuapp.com/'

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "¡Mensaje recibido!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=HEROKU_URL + BOT_TOKEN)
    return "¡Webhook configurado!", 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))