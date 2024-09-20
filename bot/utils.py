import os
import yt_dlp
from googleapiclient.discovery import build

YT_API = os.getenv('YT_Api')

def search_music(query):
    """Busca videos en YouTube relacionados con la consulta."""
    youtube = build('youtube', 'v3', developerKey=YT_API)

    # Realiza una búsqueda en YouTube
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=10,
        videoCategoryId='10'
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
        "SIDCC=AKEyXzU-V_f2F47DSDV86Am6tqUf",
        "Gt=DbrrY3pmNEItO||8YPWH-EBUeGA",
        "PREF=tz=America.Indiana/Petersburg",
        "APISID=yxmzoPCqA4SVuF95/A0AQ4Ynccukl",
        "SAPISID=myWQZPXhvoPB1ZiB/A3ugP53KKuU",
        "SID=9.a000oAhhDGcqPT9syBMMUhq2eT",
        "_Secure-PAPISID=myWQZPXhvoPB1ZiB/A3ugP53KKuU"
    ]

    with open('cookies.txt', 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This file was generated by yt-dlp\n")
        
        for cookie in raw_cookies:
            name, value = cookie.split('=', 1)
            f.write(f'.youtube.com\tTRUE\t/\t0\t{name}\t{value}\n')

format_cookies()

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