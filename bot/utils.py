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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'cookies': 'cookies.txt'
    }

    if not os.path.exists('data'):
        os.makedirs('data')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = f"data/{info['title']}.mp3"
        
        return file_path