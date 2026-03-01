import subprocess
import os
import requests
import keyboard
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values, load_dotenv
from rich import print
from groq import Groq
import webbrowser
import asyncio
import platform

# -----------------------------
# Automation Class
# -----------------------------
class Automation:
    def __init__(self):
        # Load Environment Variables
        load_dotenv()
        self.env_vars = dotenv_values(".env")
        self.GrogAPIKey = self.env_vars.get("GrogAPIKey")
        self.client = Groq(api_key=self.GrogAPIKey) if self.GrogAPIKey else None
        self.messages = []
        self.username = self.env_vars.get("Username", os.environ.get("Username", "User"))
        self.SystemChatBot = [{"role": "system", "content": f"Hello, I am {self.username}. You're a content writer."}]
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        self.os_type = platform.system()  # "Windows", "Darwin", "Linux"

    # -----------------------------
    # Google Search
    # -----------------------------
    def GoogleSearch(self, Topic):
        search(Topic)
        print(f"Google search executed for: {Topic}")
        return True

    # -----------------------------
    # Content generation using Groq
    # -----------------------------
    def Content(self, Topic):
        def OpenTextFile(File):
            try:
                if self.os_type == "Darwin":  # macOS
                    subprocess.run(["open", "-a", "TextEdit", File])
                elif self.os_type == "Windows":
                    os.startfile(File)
                elif self.os_type == "Linux":
                    subprocess.run(["xdg-open", File])
                print(f"Opened file: {File}")
            except Exception as e:
                print(f"Error opening file: {e}")

        def ContentWriterAI(prompt):
            if not self.client:
                return "Missing Groq API key."
            self.messages.append({"role": "user", "content": f"{prompt}"})
            completion = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=self.SystemChatBot + self.messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None,
            )

            Answer = ""
            for chunk in completion:
                if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")
            self.messages.append({"role": "assistant", "content": Answer})
            return Answer

        TopicClean = Topic.replace("Content", "").strip()
        ContentByAI = ContentWriterAI(TopicClean)

        filename = rf"Data/{TopicClean.lower().replace(' ', '')}.txt"
        os.makedirs("Data", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(ContentByAI)

        OpenTextFile(filename)
        return True

    # -----------------------------
    # YouTube search
    # -----------------------------
    def YoutubeSearch(self, Topic):
        Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
        webbrowser.open(Url4Search)
        print(f"YouTube search executed for: {Topic}")
        return True

    # -----------------------------
    # Play YouTube video
    # -----------------------------
    def PlayYoutube(self, query):
        playonyt(query)
        print(f"Playing YouTube video: {query}")
        return True

    # -----------------------------
    # Open App or URL
    # -----------------------------
    def OpenApp(self, app):
        try:
            if os.path.exists(app) and os.path.isfile(app):  # local file
                if self.os_type == "Darwin":
                    subprocess.run(["open", app])
                elif self.os_type == "Windows":
                    os.startfile(app)
                elif self.os_type == "Linux":
                    subprocess.run(["xdg-open", app])
            else:
                webopen(app)  # treat as URL
            print(f"Opened: {app}")
            return True
        except Exception as e:
            print(f"Error opening {app}: {e}")
            return False

    # -----------------------------
    # Close App (cross-platform)
    # -----------------------------
    def CloseApp(self, app):
        try:
            if self.os_type == "Windows":
                subprocess.run(["taskkill", "/F", "/IM", f"{app}.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif self.os_type in ["Darwin", "Linux"]:
                subprocess.run(["pkill", app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Closed: {app}")
            return True
        except Exception as e:
            print(f"Error closing {app}: {e}")
            return False

    # -----------------------------
    # System commands (volume)
    # -----------------------------
    def System(self, command):
        command = command.lower()
        try:
            if command == "mute":
                keyboard.press_and_release("volume mute")
            elif command == "unmute":
                keyboard.press_and_release("volume unmute")
            elif command == "volume up":
                keyboard.press_and_release("volume up")
            elif command == "volume down":
                keyboard.press_and_release("volume down")
            print(f"Executed system command: {command}")
            return True
        except Exception as e:
            print(f"Error executing system command {command}: {e}")
            return False

    # -----------------------------
    # Async command executor
    # -----------------------------
    async def TranslateAndExecute(self, commands: list[str]):
        funcs = []
        for command in commands:
            command = command.strip()
            if command.startswith("open") and "open it" not in command and "open file" not in command:
                fun = asyncio.to_thread(self.OpenApp, command.removeprefix("open ").strip())
                funcs.append(fun)
            elif command.startswith("close"):
                fun = asyncio.to_thread(self.CloseApp, command.removeprefix("close ").strip())
                funcs.append(fun)
            elif command.startswith("play"):
                fun = asyncio.to_thread(self.PlayYoutube, command.removeprefix("play ").strip())
                funcs.append(fun)
            elif command.startswith("content"):
                fun = asyncio.to_thread(self.Content, command.removeprefix("content ").strip())
                funcs.append(fun)
            elif command.startswith("google search"):
                fun = asyncio.to_thread(self.GoogleSearch, command.removeprefix("google search ").strip())
                funcs.append(fun)
            elif command.startswith("youtube search"):
                fun = asyncio.to_thread(self.YoutubeSearch, command.removeprefix("youtube search ").strip())
                funcs.append(fun)
            elif command.startswith("system"):
                fun = asyncio.to_thread(self.System, command.removeprefix("system ").strip())
                funcs.append(fun)
            else:
                print(f"[red]No Function Found For:[/red] {command}")

        if not funcs:
            print("No actionable commands found.")
            return False

        results = await asyncio.gather(*funcs, return_exceptions=True)
        overall_success = True
        for result in results:
            if isinstance(result, Exception):
                print(f"Task raised exception: {result}")
                overall_success = False
            elif isinstance(result, str):
                print(f"Task Result: {result}")
            elif isinstance(result, bool):
                if result is True:
                    print("Task executed successfully.")
                else:
                    print("Task failed.")
                    overall_success = False
            else:
                print(f"Unexpected result type: {type(result)}")
        return overall_success

# -----------------------------
# Testing Function
# -----------------------------
def test_automation():
    print(f"[bold green]Hello there! Jarvis this side ready to help you[/bold green]")
    auto = Automation()
    while True:
        user_input = input("\nEnter a command to test (or 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting Automation test. Goodbye!")
            break
        if user_input == "":
            print("Please enter a valid command.")
            continue

        # Split multiple commands with semicolon
        commands = [cmd.strip() for cmd in user_input.split(";")]
        asyncio.run(auto.TranslateAndExecute(commands))

# -----------------------------
# Main Entry Point
# -----------------------------
if __name__ == "__main__":
    test_automation()
