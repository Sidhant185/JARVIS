from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

class SpeechRecognition:
    def __init__(self):
        # Load environment variables from the .env files
        env_vars = dotenv_values(".env")
        self.InputLanguage = env_vars.get("InputLanguage")
        
        # Define The Html Code for the speech recognition interface
        self.HtmlCode = '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Speech Recognition</title>
        </head>
        <body>
            <button id="start" onclick="startRecognition()">Start Recognition</button>
            <button id="end" onclick="stopRecognition()">Stop Recognition</button>
            <p id="output"></p>
            <script>
                const output = document.getElementById('output');
                let recognition;

                function startRecognition() {
                    recognition = new webkitSpeechRecognition() || new SpeechRecognition();
                    recognition.lang = '';
                    recognition.continuous = true;

                    recognition.onresult = function(event) {
                        const transcript = event.results[event.results.length - 1][0].transcript;
                        output.textContent += transcript;
                    };

                    recognition.onend = function() {
                        recognition.start();
                    };
                    recognition.start();
                }

                function stopRecognition() {
                    recognition.stop();
                    output.innerHTML = "";
                }
            </script>
        </body>
        </html>'''

        # Write the modified HTML Code to a file.
        current_dir = os.getcwd()
        self.Link = f"{current_dir}/Data/voice.html"
        
        # Replace the language setting in the HTML Code with the input language from the environment variables. 
        self.HtmlCode = self.HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{self.InputLanguage}'")

        with open(self.Link, "w") as f:
            f.write(self.HtmlCode)

        # Set chrome options for the WebDriver
        self.chrome_options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
        self.chrome_options.add_argument(f'user-agent={user_agent}')
        self.chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.chrome_options.add_argument("--use-fake-device-for-media-stream")
        self.chrome_options.add_argument("--headless=new")

        # Initialize the chrome WebDriver using the chromeDriverManager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

        # Define the path for temporary files
        self.TempDirpath = f"{current_dir}/Frontend/Files"

    # Functions to set the assistant's Status by writing it to a file
    def SetAssistantStatus(self, Status):
        with open(f'{self.TempDirpath}/Staus.data', "w", encoding='utf-8') as file:
            file.write(Status)

    # Function to modify a query to ensure proper punctuation and formatting
    def QueryModifier(self, Query):
        new_query = Query.lower().strip()
        query_words = new_query.split()
        question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]

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

    # Function to translate text into English using the mtranslate library
    def UniversalTranslator(self, Text):
        self.driver.get("file:///" + self.Link)
        self.driver.find_element(by=By.ID, value="start").click()

        while True:
            try:
                Text = self.driver.find_element(by=By.ID, value="output").text

                if Text:
                    self.driver.find_element(by=By.ID, value="end").click()

                    if self.InputLanguage.lower() == "en":
                        return self.QueryModifier(Text)
                    else:
                        self.SetAssistantStatus("Translating....")
                        translated_text = mt.translate(Text, "en")
                        return self.QueryModifier(translated_text)
            except Exception as e:
                pass
if __name__ == "__main__":
    speech_recognition = SpeechRecognition()  # Instantiate the SpeechRecognition class
    while True:
        # Continuously perform speech recognition and print the recognized text
        Text = speech_recognition.UniversalTranslator("")  # Pass an empty string for the initial call
        print(Text)
