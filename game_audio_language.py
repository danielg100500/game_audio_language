import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from googletrans import Translator

duration = 5
sample_rate = 44100

print('Привет! Это игра, для изучения английского языка. Тут нужно сказать перевод слова на английском.')


words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "зонт"]
}

level = input('Какой вы уровень предпочитаете🎖️? Напишите на английском.')

word = random.choice(words_by_level[level])

start = input('Вы готовы начать? напишите yes, чтобы начать.')
if start == "yes":
    print(f"Скажи {word} на английском🎙️")
    recording = sd.rec(
    int(duration * sample_rate), # длительность записи в сэмплах
    samplerate=sample_rate,      # частота дискретизации
    channels=1,                  # 1 — это моно
    dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...💾")

    
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en - EN")

    except sr.RequestError as e:
        print(f"Ошибка сервиса: {e}📟")

    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.🔈")

    translator = Translator()
    translated = translator.translate(text, dest='ru')
    print(f'Было загаданно слово {word}, вы сказали', translated.text, '.')
    if word == translated.text:
        print('Поздравляю, вы знаете это слово😊')
    else:
        print('Вы не смогли сказать это слово🙁')
else:
    print('Перезапустите программу, чтобы играть.🎮')
