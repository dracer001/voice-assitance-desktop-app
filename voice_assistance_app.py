import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import tkinter as tk
from tkinter import messagebox

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Function for the assistant to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for commands
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        status_label.config(text="Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            status_label.config(text=f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            status_label.config(text="Listening failed")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the internet.")
            status_label.config(text="Internet connection error")
            return ""

# Function to handle commands
def handle_command(command):
    if "search" in command:
        speak("What would you like to search for?")
        search_query = listen()
        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Searching for {search_query}")

    elif "remind me" in command:
        speak("What reminder would you like to set?")
        reminder_text = listen()
        if reminder_text:
            with open("reminders.txt", "a") as file:
                file.write(f"{reminder_text} - {datetime.datetime.now()}\n")
            speak(f"Reminder set: {reminder_text}")

    elif "what is" in command or "who is" in command:
        speak("Let me search that for you.")
        try:
            answer = wikipedia.summary(command, sentences=2)
            speak(answer)
            status_label.config(text=answer)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are several entries for that topic, please be more specific.")
        except Exception:
            speak("Sorry, I couldn't find an answer to that question.")

    else:
        speak("I'm not sure how to help with that.")

# Function to start the assistant
def start_assistant():
    speak("Hello! How can I assist you today?")
    command = listen()
    handle_command(command)

# Initialize the Tkinter GUI
app = tk.Tk()
app.title("Voice Assistant")
app.geometry("400x300")

# GUI elements
title_label = tk.Label(app, text="Voice Assistant", font=("Arial", 18))
title_label.pack(pady=10)

status_label = tk.Label(app, text="Press 'Start Listening' to begin", font=("Arial", 12))
status_label.pack(pady=20)

start_button = tk.Button(app, text="Start Listening", command=start_assistant, font=("Arial", 12), bg="lightblue")
start_button.pack(pady=10)

exit_button = tk.Button(app, text="Exit", command=app.quit, font=("Arial", 12), bg="salmon")
exit_button.pack(pady=10)

# Run the Tkinter event loop
app.mainloop()
