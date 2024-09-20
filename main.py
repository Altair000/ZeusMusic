import telebot
import os
from bot.handlers import bot, register_handlers
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.environ.get('Token')

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return 'OK', 200

if __name__ == '__main__':
    # Registrar los handlers
    register_handlers(bot)

    # Configurar el webhook
    bot.remove_webhook()
    bot.set_webhook(url=f"https://zeusmusicbot-610073f53b03.herokuapp.com/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))