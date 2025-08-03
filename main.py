import tkinter as tk
from tkinter import messagebox, simpledialog
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from deep_translator import GoogleTranslator
import googletrans

# Get language data
lang = googletrans.LANGUAGES
switched_dict = {value.lower(): key for key, value in lang.items()}

# Define styling
BACKGROUND_COLOR = "#f0f4f7"
BUTTON_COLOR = "#4a90e2"
HOVER_COLOR = "#357ABD"
TEXT_COLOR = "#ffffff"
FONT = ("Segoe UI", 12)

# Utility function: speak a message in a given language
def speak_text(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("output.mp3")
        playsound("output.mp3")
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# Function: Text to Speech
def text_to_speech():
    lang_name = simpledialog.askstring("Language", "Enter language (e.g. english, hindi):")
    if not lang_name:
        return
    lang_name = lang_name.lower()
    if lang_name not in switched_dict:
        messagebox.showerror("Error", "Unsupported language.")
        return
    lang_code = switched_dict[lang_name]
    message = simpledialog.askstring("Message", "Enter the message to speak:")
    if message:
        speak_text(message, lang_code)

# Function: Speech to Text
def speech_to_text():
    recogniser = sr.Recognizer()

    spoken_lang = simpledialog.askstring("Spoken Language", "Enter the language you will speak (e.g. tamil, english):")
    if not spoken_lang:
        return
    spoken_lang = spoken_lang.lower()
    if spoken_lang not in switched_dict:
        messagebox.showerror("Error", "Unsupported spoken language.")
        return
    spoken_lang_code = switched_dict[spoken_lang]

    output_lang = simpledialog.askstring("Output Language", "Enter the language you want the text in (e.g. english, tamil):")
    if not output_lang:
        return
    output_lang = output_lang.lower()
    if output_lang not in switched_dict:
        messagebox.showerror("Error", "Unsupported output language.")
        return
    output_lang_code = switched_dict[output_lang]

    try:
        with sr.Microphone() as source:
            messagebox.showinfo("Info", f"Speak now in {spoken_lang.capitalize()}...")
            recogniser.adjust_for_ambient_noise(source, duration=1)
            audio = recogniser.listen(source, timeout=5)
            
            recognized_text = recogniser.recognize_google(audio, language=spoken_lang_code)

            if spoken_lang_code == output_lang_code:
                translated_text = recognized_text
            else:
                translator = GoogleTranslator(source=spoken_lang_code, target=output_lang_code)
                translated_text = translator.translate(recognized_text)

            messagebox.showinfo("Result", f"Recognized Text ({spoken_lang.capitalize()}):\n{recognized_text}\n\nTranslated Text ({output_lang.capitalize()}):\n{translated_text}")

            tts = gTTS(text=translated_text, lang=output_lang_code, slow=False)

    except Exception as e:
        messagebox.showerror("Speech Error", str(e))


# Function: Translate Text
def translate_text():
    src = simpledialog.askstring("Source Language", "Enter source language (e.g. english):")
    tgt = simpledialog.askstring("Target Language", "Enter target language (e.g. french):")
    if not src or not tgt:
        return
    src = src.lower()
    tgt = tgt.lower()
    if src not in switched_dict or tgt not in switched_dict:
        messagebox.showerror("Error", "Unsupported language(s).")
        return
    src_code = switched_dict[src]
    tgt_code = switched_dict[tgt]
    message = simpledialog.askstring("Input", "Enter the message to translate:")
    if message:
        try:
            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(message)
            messagebox.showinfo("Translated", translated)
            speak_text(translated, tgt_code)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

# Hover effect handlers
def on_enter(event):
    event.widget.config(bg=HOVER_COLOR)

def on_leave(event):
    event.widget.config(bg=BUTTON_COLOR)

# Initialize the GUI app
app = tk.Tk()
app.title("Speech/Text App")
app.geometry("350x350")
app.configure(bg=BACKGROUND_COLOR)

# Title
tk.Label(app, text="Speech/Text Toolkit", font=("Segoe UI", 18, "bold"),
         bg=BACKGROUND_COLOR, fg="#333").pack(pady=20)

# Create styled buttons
def create_button(text, command):
    btn = tk.Button(app, text=text, font=FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR,
                    activebackground=HOVER_COLOR, width=25, height=2, bd=0, relief="ridge",
                    command=command)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=8)
    return btn

# Add buttons
create_button("Text to Speech", text_to_speech)
create_button("Speech to Text", speech_to_text)
create_button("Translate Text", translate_text)
create_button("Exit", app.quit)

# Run the app
app.mainloop()
