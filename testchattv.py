import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import os
import pickle
import json
import urllib.parse
import urllib.request

friday = pyttsx3.init()
voices = friday.getProperty('voices')
friday.setProperty('voice', voices[1].id)

def speak(audio):
    print('F.R.I.D.A.Y: ' + audio)
    friday.say(audio)
    friday.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    speak("It is")
    speak(Time)

def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    elif hour >= 18 and hour < 24:
        speak("Good Evening sir")
    speak("How can I help you, boss")

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='vi-VN')
        print("Tony Lèo: " + query)
    except sr.UnknownValueError:
        print('Sorry sir! I didn\'t get that! Try again.')
        query = command()
    return query

def search_google(query):
    search_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={search_query}"
    wb.get().open(url)

def train_model():
    commands = {
        "google": "search on google",
        "youtube": "search on youtube",
        "quit": "quit the program",
        "open video": "open a video",
        "time": "get the current time"
    }
    dataset = []
    for cmd, description in commands.items():
        speak(f"What should I do when you say '{cmd}'?")
        user_input = command().lower()
        dataset.append((cmd, user_input))
        speak(f"Okay, I will {description} when you say '{cmd}'.")
    with open("dataset.pkl", "wb") as f:
        pickle.dump(dataset, f)
    speak("Thank you for training me!")

def load_model():
    try:
        with open("dataset.pkl", "rb") as f:
            dataset = pickle.load(f)
        return dict(dataset)
    except FileNotFoundError:
        return {}

def update_model(new_query, model):
    if new_query:
        speak("I'm sorry, I don't know how to do that. Let me search it on Google for you.")
        search_google(new_query)
        speak("Here are some search results on Google. Please tell me the correct command.")
        correct_command = command().lower()
        model[new_query] = correct_command
        with open("dataset.pkl", "wb") as f:
            pickle.dump(list(model.items()), f)
        speak("Thank you for teaching me the new command.")

if __name__ == "__main__":
    model = load_model()
    if not model:
        speak("I need to be trained first.")
        train_model()
        model = load_model()
    welcome()

    while True:
        query = command().lower()
        if query in model:
            action = model[query]
            if action == "search on google":
                speak("What should I search, boss?")
                search = command().lower()
                url = f"https://google.com/search?q={search}"
                wb.get().open(url)
                speak(f'Here is your {search} on google')
            elif action == "search on youtube":
                speak("What should I search, boss?")
                search = command().lower()
                url = f"https://youtube.com/search?q={search}"
                wb.get().open(url)
                speak(f'Here is your {search} on youtube')
            elif action == "quit the program":
                speak("Friday is off. Goodbye, boss")
                quit()
            elif action == "open a video":
                meme = r"C:\Users\Admin\Desktop\test\meme.mp4"
                os.startfile(meme)
            elif action == "get the current time":
                time()
        else:
            update_model(query, model)
