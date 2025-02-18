import subprocess
import os
import requests
import keyboard
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import asyncio

class Automation:
    def __init__(self):
        # Load Environment Variables
        self.env_vars = dotenv_values(".env")
        self.GrogAPIKey = self.env_vars.get("GrogAPIKey")
        self.client = Groq(api_key=self.GrogAPIKey)
        self.messages = []
        self.SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}. You're a content writer."}]
        self.classes = ["zCubwf", "hgKElc", "LTKOO", "sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d", "LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dNoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

    def GoogleSearch(self, Topic):
        search(Topic)
        return True

    def Content(self, Topic):
        def OpenNotepad(File):
            default_text_editor = 'open -a TextEdit'
            subprocess.run([default_text_editor, File])

        def ContentWritterAI(prompt):
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
                if chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")
            self.messages.append({"role": "assistant", "content": Answer})
            return Answer

        Topic = Topic.replace("Content", "")
        ContentByAI = ContentWritterAI(Topic)

        with open(rf"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
            file.write(ContentByAI)

        OpenNotepad(rf"Data/{Topic.lower().replace(' ', '')}.txt")
        return True

    def YoutubeSearch(self, Topic):
        Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
        webbrowser.open(Url4Search)
        return True

    def PlayYoutube(self, query):
        playonyt(query)
        return True

    def OpenApp(self, app, sess=requests.session()):
        try:
            webopen(app)
            return True
        except Exception as e:
            print(f"Error opening {app}: {e}")
            return False

    def CloseApp(self, app):
        if "chrome" in app:
            pass
        else:
            try:
                subprocess.run(["pkill", app])
                return True
            except Exception as e:
                print(f"Error closing {app}: {e}")
                return False

    def System(self, command):
        def mute():
            keyboard.press_and_release("volume mute")

        def unmute():
            keyboard.press_and_release("volume unmute")

        def volume_up():
            keyboard.press_and_release("volume up")

        def volume_down():
            keyboard.press_and_release("volume down")

        if command == "mute":
            mute()
        elif command == "unmute":
            unmute()
        elif command == "Volume up":
            volume_up()
        elif command == "Volume down":
            volume_down()

        return True

    async def TranslateAndExecute(self, commands: list[str]):
        funcs = []
        for command in commands:
            if command.startswith("open"):
                if "open it" in command:
                    pass
                elif "open file" == command:
                    pass
                else:
                    fun = asyncio.to_thread(self.OpenApp, command.removeprefix("open"))
                    funcs.append(fun)

            elif command.startswith("close"):
                fun = asyncio.to_thread(self.CloseApp, command.removeprefix("close "))
                funcs.append(fun)
            elif command.startswith("play"):
                fun = asyncio.to_thread(self.PlayYoutube, command.removeprefix("play "))
                funcs.append(fun)
            elif command.startswith("content"):
                fun = asyncio.to_thread(self.Content, command.removeprefix("content "))
                funcs.append(fun)
            elif command.startswith("google search"):
                fun = asyncio.to_thread(self.GoogleSearch, command.removeprefix("google search "))
                funcs.append(fun)
            elif command.startswith("youtube search"):
                fun = asyncio.to_thread(self.YoutubeSearch, command.removeprefix("youtube search "))
                funcs.append(fun)
            elif command.startswith("system"):
                fun = asyncio.to_thread(self.System, command.removeprefix("system "))
                funcs.append(fun)
            else:
                print(f"No Function Found For {command}")

        results = await asyncio.gather(*funcs)
        for result in results:
            if isinstance(result, str):
                print(f"Task Result: {result}")
            elif isinstance(result, bool) and result is True:
                print(f"Task executed successfully.")
            elif isinstance(result, bool) and result is False:
                print(f"Task failed.")
            else:
                print(f"Unexpected result type: {type(result)}")
