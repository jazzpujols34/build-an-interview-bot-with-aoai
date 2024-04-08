# Generative AI Engineer Interview Bot

The Interview Bot application simulates a mock interview scenario, allowing users to interact with an AI interviewer through voice responses. It leverages 
 Azure OpenAI for natural language processing, ElevenLabs for text-to-speech conversion, FastAPI for the backend, and React for the frontend.

## Key Technologies

- Azure OpenAI: Utilized for transcribing audio inputs and generating conversational responses, enhancing the AI's understanding and interaction capabilities.

- ElevenLabs API: Converts text responses from the AI into audible speech, providing a seamless conversational experience.

- FastAPI: A modern, fast web framework for building APIs.

- React: A JavaScript library for building user interfaces, enabling dynamic and responsive web applications.

- Ant Design (AntD): A comprehensive React UI library that contains a set of high-quality components and demos for building rich, interactive user interfaces.

### Prerequisites

- Python 3.10

- An Azure OpenAI account

- An ElevenLabs account

## Installation and Setup

### Backend Setup

 **Navigate to the backend directory**

```bash
cd backend_recorder
```

 **Install dependencies**

```bash
pip install -r requirements.txt
```

 **Start the FastAPI server**

```bash
uvicorn main:app --reload
```

### Frontend Setup

**Navigate to the frontend directory**

```bash
cd frontend_recorder
```

**Install NPM packages**

```bash
npm install
```

**Start the React application**

```
npm start
```

## Environment Variables

Make sure to set up your .env file in the backend directory with the following variables:

### .env file content

```
ELEVENLABS_KEY=your_elevenlabs_api_key

AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint

AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

Replace `your_elevenlabs_api_key`, `your_azure_openai_endpoint`, and `your_azure_openai_api_key` with your actual API keys and endpoint URL.

## Usage Instructions


- Record: Click the microphone button to start recording your response.

- Stop: Click the stop button to end the recording. The application will process your input and provide a response.

- Clear History: Click the "Clear History" button to reset your chat history.