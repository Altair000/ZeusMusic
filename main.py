import telebot
import os
from bot.handlers import bot
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = os.getenv('Token')
HEROKU_URL = 'https://zeusmusicbot-610073f53b03.herokuapp.com/'

# Configura el webhook
HEROKU_APP_NAME = 'zeusmusicbot-610073f53b03'  # Asegúrate de definir esto en Heroku
WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{BOT_TOKEN}"

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return 'OK', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))