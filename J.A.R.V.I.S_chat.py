import webbrowser
import os
import random
import platform
import datetime
import subprocess
import pywhatkit
from openai import OpenAI

# ----- AI SETUP (Groq Free API) -----

client = OpenAI(
    api_key="API",
    base_url="https://api.groq.com/openai/v1"
)

# Lists
stop_words = ["exit", "quit", "stop", "end", "terminate", "halt", "close"]
song_actions = ["play", "start", "listen", "turn on", "begin", "launch", "activate", "stream"]

greeting_variations = [
    "Hello boss, how can I help you?", "Hi boss, what can I do for you?",
    "Greetings boss, how may I assist you?"
]

farewell_messages = [
    "Goodbye, sir! Always happy to help!", "Take care, sir! At your service anytime!",
    "Farewell, sir! I’m always here if you need me!"
]

# ----- AI RESPONDER -----

def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a personal assistant of Sarbish chaudhary named FRIDAY."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        print("🤖", answer)

    except Exception as e:
        print("AI Error:", e)

# ----- Helpers -----

def tell_time():
    print("🕒 The time is", datetime.datetime.now().strftime('%I:%M %p'))

def tell_date():
    print("📅 Today is", datetime.datetime.now().strftime('%Y-%B-%d'))

def tell_day():
    print("📅 Today is", datetime.datetime.now().strftime('%A'))

def open_chrome():
    print("Opening Chrome...")
    if platform.system() == "Windows":
        os.system("start chrome")
    elif platform.system() == "Linux":
        os.system("google-chrome &")

def open_firefox():
    print("Opening Firefox...")
    if platform.system() == "Windows":
        os.system("start firefox")
    elif platform.system() == "Linux":
        os.system("firefox &")

def open_facebook():
    print("Opening Facebook...")
    webbrowser.open("https://www.facebook.com")

def open_youtube():
    print("Opening YouTube...")
    webbrowser.open("https://www.youtube.com")

def open_user_folder(folder):
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, folder.lower())
    
    if os.path.isdir(folder_path):
        if platform.system() == "Windows":
            subprocess.run(["explorer", folder_path])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", folder_path])
    else:
        print("Folder not found.")

def play_song(command):
    for action in song_actions:
        if action in command:
            song = command.replace(action, "").strip()
            if song:
                print(f"Playing {song} on YouTube...")
                pywhatkit.playonyt(song)
            return True
    return False

# ----- Main Chatbot -----

def run_chatbot():
    print(random.choice(greeting_variations))
    
    while True:
        command = input("💬 You: ").lower().strip()
        if not command:
            continue

        if any(word in command for word in stop_words):
            print(random.choice(farewell_messages))
            break

        elif play_song(command):
            continue

        elif "time" in command:
            tell_time()

        elif "date" in command:
            tell_date()

        elif "day" in command:
            tell_day()

        elif "chrome" in command:
            open_chrome()

        elif "firefox" in command:
            open_firefox()

        elif "facebook" in command:
            open_facebook()

        elif "youtube" in command:
            open_youtube()

        elif "folder" in command:
            folder = input("Which folder do you want to open? ")
            open_user_folder(folder)

        else:
            ask_ai(command)

if __name__ == "__main__":
    run_chatbot()