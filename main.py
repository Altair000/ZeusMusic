import telebot
import os
from bot.handlers import bot
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.environ.get('Token')

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "¡Mensaje recibido!", 200

@app.route("/" + TOKEN, methods=['POST'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://zeusmusicbot-610073f53b03.herokuapp.com/' + TOKEN)
    return "¡Webhook configurado!", 200

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))