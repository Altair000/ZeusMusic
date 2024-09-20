import telebot
import os
from bot.handlers import bot
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.environ.get('Token')

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if update:
            bot.process_new_updates([telebot.types.Update.de_json(update)])
    except Exception as e:
        print(f"Error: {e}")
    return 'OK', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://zeusmusicbot-610073f53b03.herokuapp.com/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))