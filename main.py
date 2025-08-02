import tkinter as tk
from tkinter import messagebox, simpledialog
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from deep_translator import GoogleTranslator
import googletrans

lang = googletrans.LANGUAGES
switched_dict = {value.lower(): key for key, value in lang.items()}

def speak_text(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("output.mp3")
        playsound("output.mp3")
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

def text_to_speech():
    lang_name = simpledialog.askstring("Language", "Enter language (e.g. english, hindi):").lower()
    if lang_name not in switched_dict:
        messagebox.showerror("Error", "Unsupported language.")
        return
    lang_code = switched_dict[lang_name]
    message = simpledialog.askstring("Message", "Enter the message to speak:")
    speak_text(message, lang_code)

def speech_to_text():
    recogniser = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            messagebox.showinfo("Info", "Speak now...")
            recogniser.adjust_for_ambient_noise(source)
            audio = recogniser.listen(source, timeout=5)
            result = recogniser.recognize_google(audio)
            messagebox.showinfo("You said:", result)
    except Exception as e:
        messagebox.showerror("Speech Error", str(e))

def translate_text():
    src = simpledialog.askstring("Source Language", "Enter source language (e.g. english):").lower()
    tgt = simpledialog.askstring("Target Language", "Enter target language (e.g. french):").lower()
    if src not in switched_dict or tgt not in switched_dict:
        messagebox.showerror("Error", "Unsupported language(s).")
        return
    src_code = switched_dict[src]
    tgt_code = switched_dict[tgt]
    message = simpledialog.askstring("Input", "Enter the message to translate:")
    try:
        translated = GoogleTranslator(source=src_code, target=tgt_code).translate(message)
        messagebox.showinfo("Translated", translated)
        speak_text(translated, tgt_code)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# GUI Layout
app = tk.Tk()
app.title("Speech and Text App")
app.geometry("300x250")

tk.Label(app, text="Speech/Text Toolkit", font=("Helvetica", 16)).pack(pady=10)

tk.Button(app, text="Text to Speech", width=20, command=text_to_speech).pack(pady=5)
tk.Button(app, text="Speech to Text", width=20, command=speech_to_text).pack(pady=5)
tk.Button(app, text="Translate", width=20, command=translate_text).pack(pady=5)
tk.Button(app, text="Exit", width=20, command=app.quit).pack(pady=20)

app.mainloop()
