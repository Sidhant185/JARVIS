from Backend.Model import FirstlayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.Chatbot import Chatbot
from Backend.TextToSpeech import TextToSpeech
from Backend.ImageGeneration import GenerateImages
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import speech_recognition as sr

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
AssistantName = env_vars.get("AssistantName", "Jarvis")

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# ---------------- Local Helpers ----------------
def AnswerModifier(Answer):
    lines = str(Answer).split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

def QueryModifier(Query):
    new_query = str(Query).lower().strip()
    if not new_query:
        return ""
    query_words = new_query.split()
    question_words = [
        "how", "what", "who", "where", "when", "why", "which", "whose", "whom",
        "can you", "what's", "where's", "how's"
    ]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def InitialExecution():
    try:
        os.makedirs('Data/Images', exist_ok=True)
        if not os.path.exists('Data/ChatLog.json'):
            with open('Data/ChatLog.json', 'w', encoding='utf-8') as f:
                json.dump([], f)
    except Exception as e:
        print(f"Init error: {e}")

# ------------------- Voice Input Only -------------------
def GetVoiceInput():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print(f"[{AssistantName}] Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5)
        query = r.recognize_google(audio)
        if query:
            print(f"[{AssistantName}] Heard: {query}")
            return query
    except sr.WaitTimeoutError:
        print(f"[{AssistantName}] Listening timed out. Try again.")
    except sr.UnknownValueError:
        print(f"[{AssistantName}] Could not understand audio. Try again.")
    except sr.RequestError as e:
        print(f"[{AssistantName}] STT request failed; {e}")
    except Exception as e:
        import traceback
        print("STT error:")
        traceback.print_exc()
    return None  # No fallback to text input

# ------------------- Main Execution -------------------
def MainExecution():
    ImageExecution = False
    ImageGenerationQuery = ""

    Query = GetVoiceInput()
    if not Query:
        return  # skip if no voice detected

    with open("SpeechRecognitionResult.txt", "w", encoding="utf-8") as file:
        file.write(Query)

    print(f"{Username}: {Query}")
    print(f"[{AssistantName}] Thinking...")

    Decision = FirstlayerDMM(Query)
    if isinstance(Decision, str):
        Decision = [Decision]
    print(f"Decision: {Decision}")

    Merged_query = " and ".join(
        ["".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate image" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    if ImageExecution:
        try:
            prompt_only = ImageGenerationQuery.replace("generate image", "").strip()
            print(f"[{AssistantName}] Generating images...")
            GenerateImages(prompt=prompt_only)
        except Exception as e:
            print(f"Image generation error: {e}")

    if any(i.startswith("realtime") for i in Decision):
        print(f"[{AssistantName}] Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        print(f"RealtimeSearchEngine Response: {Answer}")
        TextToSpeech(Answer)
        return True

    chatbot_instance = Chatbot()
    for Queries in Decision:
        if Queries.startswith("general"):
            print(f"[{AssistantName}] Responding...")
            QueryFinal = Queries.replace("general ", "")
            Answer = chatbot_instance.Chat(QueryModifier(QueryFinal))
            print(f"Chatbot Response: {Answer}")
            TextToSpeech(Answer)
            return True

    for Queries in Decision:
        if Queries.strip().startswith("exit"):
            print("Exiting...")
            os._exit(1)

    action_prefixes = ("open", "close", "play", "system", "content", "google search", "youtube search")
    action_commands = [q for q in Decision if q.startswith(action_prefixes)]
    if action_commands:
        print(f"[{AssistantName}] Executing tasks...")
        automation = Automation()
        try:
            success = run(automation.TranslateAndExecute(action_commands))
            if success:
                print(f"[{AssistantName}] Tasks completed successfully.")
            else:
                print(f"[{AssistantName}] Some tasks failed.")
            print(f"[{AssistantName}] Available...")
            return bool(success)
        except Exception as e:
            print(f"Automation error: {e}")
            print(f"[{AssistantName}] Available...")
            return False

# ------------------- Run Jarvis -------------------
if __name__ == "__main__":
    InitialExecution()
    while True:
        try:
            MainExecution()
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Runtime error: {e}")
        sleep(0.5)
