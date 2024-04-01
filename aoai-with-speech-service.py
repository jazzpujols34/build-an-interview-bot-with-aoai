import os
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up Azure OpenAI API credentials
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)


# Set up engine name
engine_name = "gpt-35-turbo-16k"

# Set up Azure Speech-to-Text and Text-to-Speech credentials
speech_key = os.getenv("SPEECH_KEY")
service_region = "eastus"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)
# Set up Azure Text-to-Speech language
speech_config.speech_synthesis_language = "en-NZ"
# Set up Azure Speech-to-Text language recognition
speech_config.speech_recognition_language = "en-NZ"

# Set up the voice configuration
speech_config.speech_synthesis_voice_name = "en-NZ-MollyNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Define the speech-to-text function


def speech_to_text():
    # Set up the audio configuration
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a speech recognizer and start the recognition
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)
    print("Say something...")

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Sorry, I didn't catch that."
    elif result.reason == speechsdk.ResultReason.Canceled:
        return "Recognition canceled."

# Define the text-to-speech function


def text_to_speech(text):
    try:
        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Text-to-speech conversion successful.")
            return True
        else:
            print(f"Error synthesizing audio: {result}")
            return False
    except Exception as ex:
        print(f"Error synthesizing audio: {ex}")
        return False

# Define the Azure OpenAI language generation function


def generate_text(prompt):
    response = client.chat.completions.create(
        model="gpt-35-turbo",  # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are interviewing the user for a Generative AI Engineer position.\
                                           Ask short questions that are relevant to a junior level developer.\
                                           Your name is Alex. The user is Jazz. \
                                           Keep responses under 30 words and be funny sometimes."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# Main program loop
while True:
    # Get input from user using speech-to-text
    user_input = speech_to_text()
    print(f"You said: {user_input}")

    # Generate a response using OpenAI
    prompt = f"Q: {user_input}\nA:"
    response = generate_text(prompt)
    # response = user_input
    print(f"AI says: {response}")

    # Convert the response to speech using text-to-speech
    text_to_speech(response)
