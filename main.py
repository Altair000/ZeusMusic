import os
from bot.handlers import bot
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = os.getenv('Token')
HEROKU_URL = 'https://zeusmusicbot-610073f53b03.herokuapp.com/'

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def receive_updates():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Establecer el webhook en Telegram
bot.remove_webhook()
bot.set_webhook(url=f"{HEROKU_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))