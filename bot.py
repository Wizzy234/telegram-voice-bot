import os
import telebot
import subprocess

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def convert_to_voice(input_file, output_file):
    cmd = [
        "ffmpeg", "-i", input_file,
        "-ar", "48000", "-ac", "1",
        "-c:a", "libopus",
        output_file
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@bot.message_handler(content_types=['audio', 'voice', 'video', 'video_note'])
def handle_media(message):
    file_id = (
        message.audio.file_id if message.audio else
        message.voice.file_id if message.voice else
        message.video.file_id if message.video else
        message.video_note.file_id
    )

    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    input_file = "input.tmp"
    output_file = "output.ogg"

    with open(input_file, "wb") as f:
        f.write(downloaded)

    convert_to_voice(input_file, output_file)

    with open(output_file, "rb") as f:
        bot.send_voice(message.chat.id, f)

    os.remove(input_file)
    os.remove(output_file)

bot.polling()
