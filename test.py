import webbrowser
import datetime
import json
import os
import subprocess
from openai import OpenAI

# ---------------- AI SETUP ----------------
client = OpenAI(
    api_key="API",  # 🔐 Replace with your key
    base_url="https://api.groq.com/openai/v1"
)

MEMORY_FILE = "memory.json"

# ---------------- MEMORY ----------------
# Ensure memory file exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)
    print(f"🗂️ Created {MEMORY_FILE} for storing memory!")

# Load existing memory
def load_memory():
    with open(MEMORY_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

memory = load_memory()

def remember(key, value):
    memory[key] = value
    save_memory(memory)
    print(f"🧠 I will remember that {key} is {value}")

def recall(key):
    if key in memory:
        print(f"🧠 {key} is {memory[key]}")
    else:
        print("🤖 I don't know that yet.")

# ---------------- AI FUNCTION ----------------
def ask_ai(question):
    try:
        messages = [
            {"role": "system", "content": f"You are KuKi-Kat. Memory: {memory}"},
            {"role": "user", "content": question}
        ]
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        answer = response.choices[0].message.content
        print("🤖", answer)
    except Exception as e:
        print("AI Error:", e)

# ---------------- BASIC FUNCTIONS ----------------
def tell_time():
    print("🕒 The time is", datetime.datetime.now().strftime('%I:%M %p'))

def open_youtube():
    print("Opening YouTube...")
    webbrowser.open("https://www.youtube.com")

# ---------------- APP CONTROL (MATE LINUX) ----------------
def open_app(app_name):
    try:
        if "chrome" in app_name:
            print("opening..........")
            subprocess.Popen(["google-chrome"])
        elif "firefox" in app_name:
            print("opening..........")
            subprocess.Popen(["firefox"])
        elif "vscode" in app_name or "code" in app_name:
            print("opening..........")
            subprocess.Popen(["code"])
        elif "mousepad" in app_name or "editor" in app_name:
            print("opening..........")
            subprocess.Popen(["mousepad"])
        elif "calculator" in app_name:
            print("opening..........")
            subprocess.Popen(["mate-calc"])
        elif "terminal" in app_name:
            print("opening..........")
            subprocess.Popen(["mate-terminal"])
        else:
            print("⚠️ App not recognized")
    except FileNotFoundError:
        print(f"⚠️ {app_name} is not installed or command not found")
    except Exception as e:
        print("Error opening app:", e)

# ---------------- MAIN LOOP ----------------
def run_chatbot():
    print("Hello sir! I am FRIDAY 🤖")

    while True:
        command = input("💬 You: ").lower().strip()

        if not command:
            continue
        elif command in ["exit", "quit", "bye"]:
            print("Goodbye sir!")
            break

        # TIME
        elif "time" in command:
            tell_time()

        # YOUTUBE
        elif "youtube" in command:
            open_youtube()

        # MEMORY SAVE
        elif "remember" in command:
            try:
                parts = command.replace("remember", "").strip().split(" is ")
                key = parts[0].strip()
                value = parts[1].strip()
                remember(key, value)
            except:
                print("⚠️ Use: remember name is John")

        # MEMORY RECALL
        elif "what is" in command:
            key = command.replace("what is", "").strip()
            recall(key)

        # OPEN APPS
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            open_app(app_name)

        # DEFAULT AI
        else:
            ask_ai(command)

# ---------------- RUN ----------------
if __name__ == "__main__":
    run_chatbot()