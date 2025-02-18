from Frontend.GUI import (GraphicalUserInterface, SetAssistantStatus, ShowTextToScewwn, TempDirectoryPath, SetMicrophoneStatus, AnswerModifier, QueryModifier, GetMicrophoneStatus, GetAssistantStatus)
from Backend.Model import FirstlayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import Chatbot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
AssistantName = env_vars.get("AssistantName", "Jarvis")

DefaultMessage = (
    f'{Username} : Hello {AssistantName}, How are you?\n'
    f'{AssistantName} : Welcome {Username}. I am doing well. How may I help you?'
)

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Helper Functions
def ShowDefaultChatIfNoChats():
    file_path = 'Data/ChatLog.json'
    with open(file_path, "r", encoding='utf-8') as file:
        if len(file.read()) < 5:
            with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as db_file:
                db_file.write("")
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as res_file:
                res_file.write(DefaultMessage)

def ReadChatLogJson():
    file_path = 'Data/ChatLog.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{AssistantName}: {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db_file:
        db_file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    file_path = TempDirectoryPath('Database.data')
    with open(file_path, "r", encoding='utf-8') as file:
        data = file.read()
    if data:
        with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as res_file:
            res_file.write(data)

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScewwn("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

# Main Execution Function
def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    SpeechRecognitionInstance = SpeechRecognition()
    Query = SpeechRecognitionInstance.UniversalTranslator("")
    print(f"Captured Query: {Query}")

    with open("SpeechRecognitionResult.txt", "w", encoding="utf-8") as file:
        file.write(Query)

    ShowTextToScewwn(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")

    Decision = FirstlayerDMM(Query)
    print(f"Decision: {Decision}")

    Merged_query = " and ".join(
        ["".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    if ImageExecution:
        with open(r"Frontend/Files/ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery}, True")
        try:
            subprocess.Popen(['python', r'Backend/ImageGeneration.py'], shell=False)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if any(i.startswith("realtime") for i in Decision):
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        print(f"RealtimeSearchEngine Response: {Answer}")
        ShowTextToScewwn(f"{AssistantName}: {Answer}")
        TextToSpeech(Answer)
        return True

    for Queries in Decision:
        if "general" in Queries:
            SetAssistantStatus("Thinking...")
            QueryFinal = Queries.replace("general ", "")
            Answer = Chatbot(QueryModifier(QueryFinal))
            print(f"Chatbot Response: {Answer}")
            ShowTextToScewwn(f"{AssistantName}: {Answer}")
            TextToSpeech(Answer)
            return True
        elif "exit" in Queries:
            print("Exiting...")
            os._exit(1)

# Threads
def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." not in AIStatus:
                SetAssistantStatus("Available...")
        sleep(0.1)

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    InitialExecution()
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
