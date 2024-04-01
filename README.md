# Generative AI Engineer Interview Bot

This project is a chatbot that simulates an interview for a Generative AI Engineer position. It uses Azure OpenAI's GPT-4 to generate responses to user messages and transcribes audio input from the user.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- An Azure OpenAI account
- An ElevenLabs account

### Installing

1. Clone the repository:
	```
	git clone https://github.com/jazzpujols34/build-an-interview-bot-with-aoai.git
	```
2. Install the required packages:
	```
	pip install -r requirements.txt
	```
3. Run the server:
	```
	uvicorn main:app --reload
	```

## Usage

Send a POST request to the `/talk` endpoint with an audio file. The bot will transcribe the audio, generate a response, convert the response to speech, and return the audio response.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/yourusername/yourrepository/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/yourusername/yourrepository/blob/main/LICENSE.md) file for details