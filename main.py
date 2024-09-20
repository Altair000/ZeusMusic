import os
import telebot
from flask import Flask, request
from bot.handlers import register_handlers  # Asegúrate de importar tus handlers

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
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
    bot.set_webhook(url=f"https://zeusmusicbot.herokuapp.com/{TELEGRAM_TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
