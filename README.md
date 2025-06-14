

# Jarvis Voice Assistant

Jarvis is an intelligent, speech-based assistant that can listen to your voice commands, fetch information from Wikipedia or OpenAI, and even summarize web articles using Google when needed.

## ✨ Features

- 🎤 Voice recognition using `speech_recognition`
- 📚 Wikipedia integration for quick facts
- 🤖 OpenAI GPT fallback for broader questions
- 🌐 Google search + article summarization with `newspaper3k`
- 🗣 Text-to-speech responses
- ⏰ Knows the time and basic conversation commands

## 🧠 How It Works

1. Listens to your voice input.
2. Detects commands like “who is”, “what is”, or general queries.
3. Responds using:
   - Wikipedia (primary)
   - OpenAI API (fallback if Wikipedia fails)
   - Google summary (fallback if OpenAI fails)
4. Speaks the result back to you using TTS.

## 📦 Requirements

- Python 3.8+
- `openai`
- `wikipedia`
- `speechrecognition`
- `googlesearch-python`
- `newspaper3k`
- `nltk`
- `pyaudio` (for microphone input)
- `pyttsx3` (for speech output)

Install dependencies:

```bash
pip install -r requirements.txt

Also download NLTK data:
import nltk
nltk.download('punkt')

🔑 Setup
Set your OpenAI API key as an environment variable:

bash
Copy
Edit
export OPENAI_API_KEY='your-api-key-here'
▶️ Run the Assistant
bash
Copy
Edit
python3 TARS.py
Speak your question when prompted. Try:

Who is Michael Jordan?

📁 File Structure
bash
Copy
Edit
TARS/
├── TARS.py               # Main assistant script
├── README.md             # Project overview
└── requirements.txt      # Python dependencies
🧪 Example Commands
"What is the time?"

"Who is Albert Einstein?"

"What is quantum computing?"

"Exit" or "Bye" to quit

📌 Notes
If OpenAI quota is exceeded, it gracefully falls back to Google.

Ensure you have microphone access enabled.

Some queries may require refining due to ambiguity.
