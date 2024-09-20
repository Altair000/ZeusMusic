import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils import search_music, download_music
from bot.buttons import create_quality_buttons

TOKEN = os.getenv('Token')
bot = telebot.TeleBot(TOKEN)

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        """Manejo del comando /start."""
        markup = InlineKeyboardMarkup()
        info_button = InlineKeyboardButton("Info", callback_data="info")
        developer_button = InlineKeyboardButton("Desarrollador", url="https://t.me/alltallr")
        markup.add(info_button, developer_button)
    
        bot.send_message(message.chat.id, "¡Bienvenido al bot de descarga de música!", reply_markup=markup)

    # Almacenar resultados para usar después
    user_search_results = {}

    # Manejador de mensajes (búsqueda de canciones)
    @bot.message_handler(func=lambda message: not message.text.startswith('/'))
    def handle_message(message):
        query = message.text
        results = search_music(query)

        user_search_results[message.chat.id] = results  # Almacenar resultados por usuario

        markup = InlineKeyboardMarkup()
        for idx, song in enumerate(results):
            markup.add(InlineKeyboardButton(f"{idx + 1}. {song['title']}", callback_data=f"song_{idx}"))

        bot.send_message(message.chat.id, "Elige una canción:", reply_markup=markup)

    # Callback para seleccionar calidad de la canción
    @bot.callback_query_handler(func=lambda call: call.data.startswith('song_'))
    def ask_quality(call):
        song_id = int(call.data.split('_')[1])
        quality_buttons = [
            InlineKeyboardButton("128 kbps", callback_data=f"quality_{song_id}_128"),
            InlineKeyboardButton("192 kbps", callback_data=f"quality_{song_id}_192"),
            InlineKeyboardButton("320 kbps", callback_data=f"quality_{song_id}_320"),
        ]
    
        markup = InlineKeyboardMarkup()
        markup.add(*quality_buttons)
        bot.send_message(call.message.chat.id, "Elige la calidad del audio:", reply_markup=markup)

    # Enviar el archivo MP3 después de seleccionar calidad
    @bot.callback_query_handler(func=lambda call: call.data.startswith('quality_'))
    def send_song(call):
        song_id, quality = map(int, call.data.split('_')[1:])
    
        # Obtener la URL del video desde los resultados almacenados
        results = user_search_results.get(call.message.chat.id)
        if results and 0 <= song_id < len(results):
            video_url = results[song_id]['url']
            mp3_file = download_music(video_url, quality)

            # Verificar tamaño del archivo antes de enviarlo
            if os.path.getsize(mp3_file) > 50 * 1024 * 1024:  # 50MB
                bot.send_message(call.message.chat.id, "El archivo es demasiado grande para descargarlo.")
            else:
                with open(mp3_file, 'rb') as audio:
                    bot.send_audio(call.message.chat.id, audio)
        else:
            bot.send_message(call.message.chat.id, "Ocurrió un error al procesar tu solicitud.")