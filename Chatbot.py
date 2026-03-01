from groq import Groq  # Importing the Grog library to use its API
from json import loads, dump  # Importing the loads and dumps to read and write JSON files
import datetime  # Importing datetime for real-time data
from dotenv import dotenv_values  # Import dotenv to load environment variables from a .env file

# Load Environment Variables from .env file
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key
Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GrogAPIKey = env_vars.get("GrogAPIKey")

# Initialize the Grog API Client Using the Provided API Key
client = Groq(api_key=GrogAPIKey)

# Define a system message that provides context to the AI chatbot about its role and behavior
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatbot = [
    {"role": "system", "content": System}
]

# Chatbot Class Definition
class Chatbot:
    def __init__(self):
        self.messages = []  # Initialize an empty list to store chat messages
        
        # Attempt to load the chat log from the JSON File
        try:
            with open(r"Data/ChatLog.json", "r") as f:
                self.messages = loads(f.read())  # Load the chat log from the JSON file
        except FileNotFoundError:
            # If the file is not found, create a new file with an empty list
            with open(r"Data/ChatLog.json", "w") as f:
                dump([], f)

    def RealtimeInformation(self):
        current_date_time = datetime.datetime.now()  # Get the current date and time
        day = current_date_time.strftime("%A")  # Get the current day
        date = current_date_time.strftime("%d")  # Get the current date
        month = current_date_time.strftime("%B")  # Get the current month
        year = current_date_time.strftime("%Y")  # Get the current year
        hour = current_date_time.strftime("%H")  # Get the current hour
        minute = current_date_time.strftime("%M")  # Get the current minute
        second = current_date_time.strftime("%S")  # Get the current second

        # Format the information into a string
        data = f"Please use the real-time information if needed,\n"
        data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
        data += f"Time: {hour} hours : {minute} minutes : {second} seconds\n"
        return data

    # Function to modify the chatbot's response for better formatting and readability
    def AnswerModifier(self, Answer):
        lines = Answer.split("\n")  # Split the answer into lines
        non_empty_lines = [line for line in lines if line.strip() != ""]  # Remove empty lines
        modified_answer = "\n".join(non_empty_lines)  # Join the non-empty lines
        return modified_answer

    # Main function to interact with the user
    def Chat(self, Query):
        """This function sends the user's query to the chatbot and returns the AI's response."""
        try:
            # Append the user's query to the messages list
            self.messages.append({"role": "user", "content": f"{Query}"})

            # Make a request to the Grog API to generate a response
            completion = client.chat.completions.create(
                model="llama3-70b-8192",  # Specify the model to use
                messages=SystemChatbot + [{"role": "system", "content": self.RealtimeInformation()}] + self.messages,  # Include system information
                max_tokens=1024,  # Limit the max tokens
                temperature=0.7,  # Set creativity level
                top_p=1.0,  # Set nucleus sampling probability
                stream=True  # Enable streaming if supported
            )

            Answer = ""  # Initialize an empty string to store the AI's response

            # Process the streamed response chunks
            for chunk in completion:
                if chunk.choices[0].delta.content:  # Check if there is content in the response chunk
                    Answer += chunk.choices[0].delta.content  # Append the response chunk to the answer

            Answer = Answer.replace("</s>", "\n")  # Clean up any unwanted token from the response

            # Append the chatbot's response to the messages list
            self.messages.append({"role": "assistant", "content": Answer})

            # Save the updated chat log to the JSON file
            with open(r"Data/ChatLog.json", "w") as f:
                dump(self.messages, f, indent=4)

            # Return the formatted response
            return self.AnswerModifier(Answer=Answer)

        except Exception as e:
            # Handle errors by printing the exception and resetting the chat log
            print(f"Error: {e}")
            with open(r"Data/ChatLog.json", "w") as f:
                dump([], f, indent=4)
            return self.Chat(Query)  # Retry the query after resetting the chat log

# Main program entry point
if __name__ == "__main__":
    chatbot = Chatbot()  # Instantiate the Chatbot class
    while True:
        user_input = input("Enter Your Question: ")  # Prompt the user for a question
        print(chatbot.Chat(user_input))  # Print the response from the AI model
