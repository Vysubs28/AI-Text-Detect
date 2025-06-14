import speech_recognition as sr
import wikipedia
import openai
from googlesearch import search
from newspaper import Article
import nltk
nltk.download('punkt', quiet=True)  # Download punkt tokenizer for newspaper
nltk.download('punkt_tab')
import os
import time
import subprocess
from datetime import datetime

# Set your OpenAI API key via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use subprocess to run 'say' cleanly on macOS
def speak(text):
    clean_text = text.strip()
    print("Assistant:", clean_text)
    subprocess.run(['say', '-v', 'Daniel', clean_text], check=True)
    time.sleep(0.2)  # small pause to avoid cutting off audio

# Listen and recognize speech with ambient noise calibration
def recognize_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        print("Calibrating for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=4)

    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: '{command}'")
        return command.lower().strip()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

# Remove repeated consecutive words (like "bye bye bye" -> "bye")
def clean_command(command):
    words = command.split()
    cleaned_words = []
    for w in words:
        if len(cleaned_words) == 0 or w != cleaned_words[-1]:
            cleaned_words.append(w)
    return " ".join(cleaned_words)

# Query OpenAI GPT-4
def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI error:", e)
        return "Sorry, I couldn't get an answer from OpenAI."

def get_google_summary(query):
    try:
        for result in search(query, num_results=3):
            return f"I found this link that might help: {result}"
        return "I couldn't find anything useful on Google."
    except Exception as e:
        print("Google search error:", e)
        return "Google search failed."
    
def get_google_summary(query):
    try:
        for result in search(query, num_results=1):
            article = Article(result)
            article.download()
            article.parse()
            article.nlp()
            # Use OpenAI to summarize article text with fallback
            summary = openai_summarize(article.text)
            return summary
        return "I couldn't find anything useful on Google."
    except Exception as e:
        print("Google summary error:", e)
        return "I tried to search Google but something went wrong."

    
def openai_summarize(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following text briefly:\n\n{text}"}
            ],
            max_tokens=150,
            temperature=0.5,
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print("OpenAI summarize error:", e)
        # fallback: just return the first 2-3 sentences of the text as a simple summary
        return ' '.join(text.split('. ')[:3]) + '.'

    
# Handle user commands and respond accordingly
def handle_command(command):
    if not command:
        speak("I didn't catch that. Please try again.")
        return

    if "exit" in command or "bye" in command:
        speak("Goodbye!")
        exit()

    if "time" in command:
        speak("The time is " + datetime.now().strftime("%I:%M %p"))
        return

    if "who is" in command or "what is" in command:
        query = command.replace("who is", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            if summary:
                speak(summary)
            else:
                raise wikipedia.exceptions.PageError(query, "No summary found")
        except wikipedia.exceptions.DisambiguationError:
            speak("That was too vague. Can you be more specific?")
        except wikipedia.exceptions.PageError:
            speak("Let me check online.")
            ai_answer = get_openai_response(command)
            if not ai_answer or "couldn't get an answer" in ai_answer.lower() or "sorry" in ai_answer.lower():
                speak("Let me check Google for a summary.")
                google_summary = get_google_summary(query)
                speak(google_summary)
            else:
                speak(ai_answer)
        except Exception:
            speak("Something went wrong. Let me check Google.")
            google_summary = get_google_summary(query)
            speak(google_summary)
        return

    # Default: use OpenAI for other queries
    ai_response = get_openai_response(command)
    speak(ai_response)


    # Default: query OpenAI for everything else
    ai_response = get_openai_response(command)
    if "couldn't get an answer" in ai_response.lower() or "sorry" in ai_response.lower():
        speak("Let me check Google.")
        google_result = get_google_summary(query)
        speak(google_result)

    else:
        speak(ai_response)



# Main loop — runs the assistant continuously
def run_assistant():
    speak("Jarvis is ready. Ask me anything.")
    while True:
        command = recognize_audio()
        command = clean_command(command)  # Remove repeated consecutive words
        handle_command(command)

if __name__ == "__main__":
    run_assistant()




