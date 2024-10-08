import os
import telebot
from flask import Flask, request
from bot.handlers import register_handlers # Asegúrate de importar tus handlers

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "¡Mensaje recibido!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://zeusmusicbot-610073f53b03.herokuapp.com/' + TOKEN)
    return "¡Webhook configurado!", 200

# Main
if __name__ == "__main__":
      register_handlers(bot)
      app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))