from googlesearch import search
from groq import Groq  # Importing the Grog library to use its API
from json import loads, dump  # Importing the loads and dumps to read and write JSON files
import datetime  # Importing datetime for real-time data
from dotenv import dotenv_values  # Import dotenv to load environment variables from a .env file

# Load Environment Variables from .env file
env_vars = dotenv_values(".env")

# Retrieve Environment variables for the chatbot configuration
Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GrogAPIKey")

# Initialize the Grog API Client Using the Provided API Key
client = Groq(api_key=GroqAPIKey)

# Define the system Instructions for the chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from the JSON file, or create an empty one if it doesn't exist
try:
    with open(r"Data/ChatLog.json", "r") as f:
        messages = loads(f.read())  # Read file content as string and load it as JSON
except:
    with open(r"Data/ChatLog.json", "w") as f:
        dump([], f)  # Create an empty chat log if file doesn't exist

# Function to perform a Google search and format the results 
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The Search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"  # Changed 'tittle' to 'title'

    Answer += "[end]"
    return Answer


# Function to clean up the answer by removing empty lines
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

# Predefined chatbot Conversation system message and an initial chat history
SystemChatbot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, How can I help you today?"},
]

# Function to get real-time information like the current date and time
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y") 
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"use this Real-time information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds\n"
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatbot, messages

    # Load the chat log from the JSON file.
    with open(r"Data/ChatLog.json", "r") as f:
        messages = loads(f.read())  # Read file content as string and load it as JSON
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google Search results to the system chatbot messages.
    SystemChatbot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq Client
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatbot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None 
    )

    Answer = ""

    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    
    # Clean up the response
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log to the JSON file
    with open(r"Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    
    # Remove the most recent system message from the chatbot conversation.
    SystemChatbot.pop()
    return AnswerModifier(Answer=Answer)

# Main Entry point of the program for interactive chatbot conversation.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
