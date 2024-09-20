#import telebot
import os
import yt_dlp
from googleapiclient.discovery import build

#TOKEN = os.getenv('Token')
#bot = telebot.TeleBot(TOKEN)

YT_API = os.getenv('YT_Api')
#chat_id = message.chat.id

def search_music(query):
    """Busca videos en YouTube relacionados con la consulta."""
    youtube = build('youtube', 'v3', developerKey=YT_API)

    # Realiza una búsqueda en YouTube
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=10
    )
    response = request.execute()

    # Extraer la información relevante (título y videoId)
    results = []
    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        live_status = item['snippet']['liveBroadcastContent']
        # Filtrar videos en estreno o en vivo
        if live_status == 'none':  # Solo videos que no son estrenos ni en vivo
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            results.append({
                'title': video_title,
                'url': video_url
            })
    
    return results

def format_cookies():
    # Simulación de las cookies de entrada como una lista de cadenas
    raw_cookies = [
      "SID=g.a000oQgjBHY3gzfE9FFVTPJhKzOEhF1Wogfy4Kb9JLrt3nziBseQ4kRJl7EOfbA3o_XwKb17iQACgYKAaYSARcSFQHGX2MilP07jdT4R03x1jD0Zwhx0xoVAUF8yKpV39-1yO1MH8__q1doXOQB0076",
      "HSID=A2NnZNqSDtngwEsLE",
      "SSID=A3YTB-7HuHcZvHMas",
      "APISID=zE8J0TbH0qhzUmio/A5bueny_hwYPxDaRn",
      "SAPISID=wO5O0tVaRmz9x4xw/A5mkJfPl9uNEexu8v",
      "PREF=tz=America.Chicago",
      "SIDCC=AKEyXzVJ6WVH7BqLb4EsLHvb1eKFz__y_v54K3Re38IixSjtwJerfRXwJ1-kcui9fLp7XeRz",
      "_Secure-3PAPISID=wO5O0tVaRmz9x4xw/A5mkJfPl9uNEexu8v",
      "_Secure-3PSID=g.a000oQgjBHY3gzfE9FFVTPJhKzOEhF1Wogfy4Kb9JLrt3nziBseQAqt7ol-HweeLxWZOWk9iyAACgYKAXwSARcSFQHGX2MiHraUPvjzlgn2npYPmCzMUhoVAUF8yKprC_oLh5hbx3aUq_dpgegt0076",
      "LOGIN_INFO=AFmmF2swRQIgbTb5aUUpj4e8etclX9IitSXi0dnb7wgm9Q88xjaY5s4CIQCEW6KqPoIqH0sOTN6rCWXr8WVALcfCWLLTHSBphEgdeA:QUQ3MjNmekhndG1sbEVjUHJDOXN4UWNiS1Q4WHFWTkowV1FuSUdELThpQ2JBTU5hRnF5WGtBaTNpOGNGVzk0dkd2WTFZUjhCNmVuSkFwQXk3OUtMeG9CMFN2TG5MbFBnQUxCVHNzMW9JcGpZVlBtS0RTbllacmFmZTNrWjNPT0pBY2RpOXlxLW5hZnI3a3MxZTJiUldfMmo3elVSSzFZRzJR"
      ]

    with open('cookies.txt', 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This file was generated by yt-dlp\n")
        
        for cookie in raw_cookies:
            name, value = cookie.split('=', 1)
            f.write(f'.youtube.com\tTRUE\t/\t0\t{name}\t{value}\n')

def verify_cookies():
    if not os.path.exists('cookies.txt'):
        print("El archivo cookies.txt no se encontró.")
        return False
    
    with open('cookies.txt', 'r') as f:
        content = f.readlines()
        
        if len(content) < 3:  # Comprobamos que hay más de las líneas de cabecera
            print("El archivo de cookies está vacío o incompleto.")
            return False

    print("Las cookies se han creado correctamente.")
    return True

# Formatear y verificar las cookies
format_cookies()
# Supón que tienes el bot y chat_id del usuario ya definidos
if verify_cookies():
    print("El archivo de cookies está listo para usarse.")
else:
    print("Hubo un problema con el archivo de cookies.")

def download_music(video_url, quality):
    
    """Descarga el audio del video de YouTube y retorna la ruta del archivo MP3."""
    ydl_opts = {
        'format': f'bestaudio[abr<={quality}]',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': str(quality),
        }],
        'outtmpl': 'data/%(title)s.%(ext)s',
        'noplaylist': True,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'cookiefile': 'cookies.txt'
    }

    if not os.path.exists('data'):
        os.makedirs('data')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = f"data/{info['title']}.mp3"
        
        # Elimina el archivo de cookies temporal
        os.remove('cookies.txt')
        
        return file_path