from telebot import types

def create_quality_buttons(video_url):
    """Crear botones in-line para seleccionar la calidad del MP3."""
    markup = types.InlineKeyboardMarkup()
    
    qualities = ['128', '192', '320']  # Opciones de calidad
    for quality in qualities:
        button = types.InlineKeyboardButton(f"Calidad {quality} kbps", callback_data=f"download_{video_url}_{quality}")
        markup.add(button)
    
    return markup

def create_info_buttons():
    """Botones para el menú de información con opción de retroceder."""
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Retroceder", callback_data="back")
    markup.add(back_button)
    
    return markup