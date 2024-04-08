from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests
import json
import os


load_dotenv()
# Define the endpoint and API key from environment variables

elevenlabs_key = os.getenv("ELEVENLABS_KEY")
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)
deployment_id = "whisper" 


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 1. Send in audio, and have it transcribed
@app.post("/talk")
async def post_audio(file: UploadFile):
    user_message = transcribe_audio(file)
    chat_response = get_chat_response(user_message)
    audio_output = text_to_speech(chat_response)

    def iterfile():
        yield audio_output  

    return StreamingResponse(iterfile(), media_type="application/octet-stream")#audio/mp3


@app.get("/clear")
async def clear_history():
    file = 'database.json'
    with open(file, 'w') as f:
        json.dump("", f)
    return {"message": "Chat history has been cleared"}

def transcribe_audio(file):
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    result = client.audio.transcriptions.create(
	file=open(file.filename, "rb"),            #audio_test_file
	model=deployment_id
)

    # Send the POST request
    transcript = result.text
    print(transcript)
    return transcript


# 2. Send the transcribe to chatgpt and get a response
def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    #   print(messages)

    # Send to ChatGpt
    gpt_response = client.chat.completions.create(
        model="gpt-35-turbo", 
        messages=messages
    )

    parsed_gpt_response = gpt_response.choices[0].message.content

    print(parsed_gpt_response)

    # Save messages
    save_messages(user_message,parsed_gpt_response)

    return parsed_gpt_response


def load_messages():
    messages = []
    file = 'database.json'

    # If file is empty we need to add the context
    empty = os.stat(file).st_size == 0

    # If file is not empty, loop through history and add to messages
    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {"role": "system", "content": "You are interviewing the user for a Generative AI Engineer position.\
                    Ask short questions that are relevant to a junior level developer.\
                    Your name is Alex. The user is Jazz. \
                    Keep responses under 30 words and be funny sometimes."},
        )
    return messages


# 3. Save the chat history adn send back and forth for context.
def save_messages(transcript, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": transcript})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)

def text_to_speech(text):
        voice_id = "pNInz6obpgDQGcFmaJgB"

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}" 

        
        headers = {
              "Content-Type": "application/json",
              "Accept": "audio/mpeg",
              "xi-api-key": elevenlabs_key
        }

        body = {
            "model_id": "eleven_monolingual_v1",
            "text": text,
            "voice_settings": {
                "similarity_boost": 0.5,    
                "stability": 0.5,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }

        try:
            response = requests.post(url, json=body, headers=headers)
            if response.status_code == 200:
                return response.content
            else:
                print("Something went wrong. Status code:", response.status_code)
                print("Error details:", response.text)
        except Exception as e :
            print(e)
