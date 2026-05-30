import pyttsx3

class VoiceAssistant:
    def __init__(self, lang_code: str):
        self.engine = pyttsx3.init()
        self.set_language(lang_code)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def set_language(self, lang_code: str):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if lang_code in voice.languages:
                self.engine.setProperty('voice', voice.id)

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    bot = VoiceAssistant("pl")
    bot.speak("Mój język mówiony jest ustawiony na polski.")