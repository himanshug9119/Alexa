import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                talk(command)
                return command
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return None

def run_alexa():
    while True:
        command = take_command()
        if command:
            if 'play' in command:
                song = command.replace('play', '')
                talk('playing ' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                current_time = datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + current_time)
            elif 'who is ' in command:
                person = command.replace('who is ', '')
                info = wikipedia.summary(person, 2)
                print(info)
                talk(info)
            elif 'jokes' in command:
                talk(pyjokes.get_joke())
            elif 'open' in command and ('app' in command or 'application' in command):
                app_name = command.replace('open', '').replace('app', '').replace('application', '').strip()
                try:
                    os.system(f'start {app_name}.exe')  # Replace with the actual command to open the app on your system
                    talk(f'Opening {app_name}')
                except Exception as e:
                    talk(f"Sorry, I couldn't open {app_name}.")
                    print(e)
            elif 'exit' in command or 'quit' in command:
                talk('Goodbye!')
                break
            else:
                talk('Please say the command again.')

if __name__ == "__main__":
    talk("Hello, I'm Alexa, what can I do for you?")
    run_alexa()
