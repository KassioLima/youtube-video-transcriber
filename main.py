from pytube import YouTube
import os
import speech_recognition as sr
from pydub import AudioSegment
import datetime
from open_ai_service import refinarTexto
import asyncio


async def _onDownloadComplete(fileName: str):
    # Converte o arquivo para WAV
    sound = AudioSegment.from_file(fileName + ".mp4", format="mp4")
    sound.export(fileName + ".wav", format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(fileName + ".wav") as source:
        audio_data = r.record(source)
        print("Transcrevendo...")
        text = r.recognize_google(audio_data, language='pt-BR')

        text = await refinarTexto(text)

        print("\nTrancrição:\n\"" + text + '"')


def _removeFiles():
    # Defina o caminho da pasta que você deseja excluir os arquivos
    pasta = "audios"

    # Use o método listdir() para obter uma lista de todos os arquivos na pasta
    arquivos = os.listdir(pasta)

    # Use um loop for para percorrer a lista de arquivos e excluí-los um por um
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta, arquivo)
        os.remove(caminho_arquivo)

    while len(os.listdir(pasta)) > 0:
        continue

async def transcrever(video_url: str):
    fileName = "audios/" + str(datetime.datetime.now().now()).replace(":", "_").replace("-", "_").replace(".", "_").replace(" ", "_").replace("_", "")

    try:
        _removeFiles()

        # Baixa o vídeo
        yt = YouTube(video_url)

        # Seleciona a primeira stream de áudio disponível e faz o download
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename=fileName + ".mp4")

        print("Escutando o vídeo...")
        while not os.path.exists(fileName + ".mp4"):
            continue

        await _onDownloadComplete(fileName)
        _removeFiles()

    except Exception as e:
        _removeFiles()
        print(e)


asyncio.run(transcrever("https://www.youtube.com/watch?v=mWzMddqkyV8"))
