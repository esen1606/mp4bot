from telebot import telebot
from telebot import types
import os

TOKEN = '6386918436:AAFZSvx_prH3M2hlRYIoakDHMUZFztJBgf0'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.username
    bot.send_message(message.chat.id, f"Добро пожаловать, @{name}!")

@bot.message_handler(commands=['music'])
def send_music(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Идет загрузка, это займет какое-то время!')
    music_folder = os.path.join(os.getcwd(), 'music_folder')  

    if os.path.exists(music_folder):
        try:
            music_files = [f for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))]
            
            if music_files:
                for file in music_files:
                    audio_path = os.path.join(music_folder, file)
                    with open(audio_path, 'rb') as audio:
                        bot.send_audio(chat_id, audio, title=file)
            else:
                bot.send_message(chat_id, "В папке нет музыкальных файлов.")
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка при чтении файлов музыки: {e}")
    else:
        bot.send_message(chat_id, "Папка с музыкой не найдена. Пожалуйста, убедитесь в наличии папки 'music_folder' в папке вашего бота.")

if __name__ =="__main__":
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(e)
