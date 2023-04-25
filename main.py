from pytube import YouTube
import os
import speech_recognition as sr
from pydub import AudioSegment
import datetime

def _onDownloadComplete(fileName: str):
    # Converte o arquivo para WAV
    sound = AudioSegment.from_file(fileName + ".mp4", format="mp4")
    sound.export(fileName + ".wav", format="wav")

    os.remove(fileName + ".mp4")

    r = sr.Recognizer()
    with sr.AudioFile(fileName + ".wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='pt-BR')
        print(text)

        os.remove(fileName + ".wav")

def transcrever(video_url: str):
    fileName = str(datetime.datetime.now().now()).replace(":", "_").replace("-", "_").replace(".", "_").replace(" ", "_").replace("_", "")

    if os.path.exists(fileName + ".mp4"):
        os.remove(fileName + ".mp4")
        while os.path.exists(fileName + ".mp4"):
            continue

    if os.path.exists(fileName + ".wav"):
        os.remove(fileName + ".wav")
        while os.path.exists(fileName + ".wav"):
            continue

    # Baixa o vídeo
    yt = YouTube(video_url)

    # Seleciona a primeira stream de áudio disponível e faz o download
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=fileName + ".mp4")

    while not os.path.exists(fileName + ".mp4"):
        continue

    _onDownloadComplete(fileName)


try:
    transcrever("https://www.youtube.com/watch?v=mWzMddqkyV8")
except Exception as e:
    print(e)