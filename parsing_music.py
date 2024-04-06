import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.last.fm/music/+free-music-downloads'

def parse_mp3party(url):
    response = requests.get(url)
    print(response)

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tracks = []
            count = 0
            for track in soup.find_all('div', class_="col-main"):
                if count >= 10:
                    break 
                title = track.find('td', class_="chartlist-name").text.strip()
                music = track.find('a', class_='chartlist-download-button')
                if music:
                    href = music.get('href')
                else:
                    href = None
                
                tracks.append({'title': title, 'music': href, })
                count += 1
                
            return tracks
        
        else:
            print("Error: Unable to fetch data from the website.")
            return []
    
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)
        return None
def download_audio(tracks):
    if not os.path.exists("music_folder2"):
        os.makedirs("music_folder2")
    
    for track in tracks:
        title = track['title']
        music_url = track['music']
        if music_url:
            try:
                audio_content = requests.get(music_url).content
                _, extension = os.path.splitext(music_url)
                if extension == '.mp3':
                    with open(f"music_folder2/{title}.mp3", 'wb') as audio_file:
                        audio_file.write(audio_content)
                    print(f"{title}.mp3 успешно скачан и сохранен.")
                else:
                    print(f"Ошибка: {title} не является аудиофайлом MP3.")
            except Exception as e:
                print(f"Ошибка при скачивании и сохранении {title}.mp3:", e)
        else:
            print(f"Для трека {title} отсутствует ссылка на аудиофайл.")
parsed_data = get_html(url)
if parsed_data:
    download_audio(parsed_data)