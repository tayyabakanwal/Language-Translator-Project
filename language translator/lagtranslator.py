import tkinter as tk
from tkinter import ttk  # For Combobox
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
from langdetect import detect
import pycountry

pygame.mixer.init()  # Audio player init

translator = Translator()
input_audio_file = "input_audio.wav"
translated_audio_file = "translated_audio.mp3"

# --- Helper Functions ---

def getLangName(lang_code):
    try:
        language = pycountry.languages.get(alpha_2=lang_code)
        return language.name
    except:
        return "Unknown"

def record_audio(filename):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="yellow")
        root.update()
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    return audio

def recognize_audio(audio):
    try:
        status_label.config(text="Recognizing...", fg="green")
        root.update()
        return sr.Recognizer().recognize_google(audio)
    except:
        status_label.config(text="Could not recognize speech!", fg="red")
        root.update()
        return None

def play_audio(file_path):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# --- Capture Input Sentence ---
def capture_input():
    global input_text, detected_lang
    audio = record_audio(input_audio_file)
    input_text = recognize_audio(audio)

    if input_text:
        lang_code = detect(input_text)
        detected_lang = getLangName(lang_code)
        status_label.config(text=f"Recorded in {detected_lang}", fg="white")
        input_text_label.config(text=f"Your Sentence: {input_text}")
        play_input_btn.pack(pady=5)
    else:
        status_label.config(text="No valid speech detected!", fg="red")

# --- Translate & Generate Output Audio ---
def translate_and_generate():
    global input_text, target_lang_code
    if input_text and target_lang_code:
        translated_text = translator.translate(input_text, dest=target_lang_code).text
        tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
        tts.save(translated_audio_file)
        status_label.config(text="Translation Ready!", fg="lightgreen")
        play_output_btn.pack(pady=5)
    else:
        status_label.config(text="Input text or language not set!", fg="red")

# --- Languages List ---
all_languages = ('afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 
                 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese', 'chinese (traditional)', 'corsican', 
                 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 
                 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 
                 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 
                 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 'latvian', 
                 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 
                 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 
                 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 
                 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 
                 'turkish', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu')

# --- Mapping for language codes ---
languages_dict = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az',
    'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca',
    'cebuano': 'ceb', 'chichewa': 'ny', 'chinese': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co',
    'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo',
    'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl',
    'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha',
    'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is',
    'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw',
    'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky',
    'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk',
    'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr',
    'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps',
    'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru',
    'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd',
    'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su',
    'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr',
    'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
    'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

# --- GUI Setup ---
root = tk.Tk()
root.title("Audio Language Translator")
root.geometry("750x550")
root.configure(bg="#2c3e50")

title_label = tk.Label(root, text="Audio Language Translator", font=("Arial", 28, "bold"), fg="#f1c40f", bg="#2c3e50")
title_label.pack(pady=20)

status_label = tk.Label(root, text="Press a button to start...", font=("Arial", 16), fg="white", bg="#2c3e50")
status_label.pack(pady=10)

# Input Section
record_btn = tk.Button(root, text="🎤 Record Input Audio", font=("Arial", 16, "bold"), bg="#27ae60", fg="white",
                       activebackground="#2ecc71", activeforeground="white", command=capture_input)
record_btn.pack(pady=15)

input_text_label = tk.Label(root, text="", font=("Arial", 14), fg="white", bg="#2c3e50")
input_text_label.pack(pady=5)

play_input_btn = tk.Button(root, text="▶ Play Your Audio", font=("Arial", 14, "bold"), bg="#8e44ad", fg="white",
                           activebackground="#9b59b6", activeforeground="white", command=lambda: play_audio(input_audio_file))
play_input_btn.pack(pady=5)  # Initially pack it, or pack it in capture_input

# Language Selection Section
language_label = tk.Label(root, text="Select Target Language:", font=("Arial", 14), fg="lightblue", bg="#2c3e50")
language_label.pack(pady=5)

language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, values=list(all_languages), state="readonly")
language_combobox.pack(pady=10)
language_combobox.bind("<<ComboboxSelected>>", lambda event: on_language_select())

def on_language_select():
    global target_lang_code, selected_language
    selected_language = language_var.get().lower()  # Get selected language
    if selected_language in languages_dict:
        target_lang_code = languages_dict[selected_language]
        language_text_label.config(text=f"Target Language: {selected_language.capitalize()}")
        status_label.config(text=f"Language Selected: {selected_language.capitalize()}", fg="lightblue")
        translate_and_generate()  # Auto trigger translation
    else:
        status_label.config(text="Language selection error!", fg="red")

language_text_label = tk.Label(root, text="", font=("Arial", 14), fg="lightblue", bg="#2c3e50")
language_text_label.pack(pady=5)

play_output_btn = tk.Button(root, text="▶ Play Translated Audio", font=("Arial", 14, "bold"), bg="#e67e22", fg="white",
                            activebackground="#d35400", activeforeground="white", command=lambda: play_audio(translated_audio_file))
play_output_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", font=("Arial", 14, "bold"), bg="#e74c3c", fg="white",
                     activebackground="#c0392b", activeforeground="white", command=root.destroy)
exit_btn.pack(pady=20)

input_text = None
detected_lang = None
target_lang_code = None
selected_language = None

root.mainloop()
