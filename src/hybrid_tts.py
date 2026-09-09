import pyttsx3
from gtts import gTTS
import os

class HybridTTS:
    def __init__(self):
        self.offline_engine = pyttsx3.init()

    def speak(self, text, online_mode=False):
        if not text:
            return

        if online_mode:
            print("[TTS] Generating Online Google Voice...")
            try:
                tts = gTTS(text=text, lang='en', tld='co.in')
                tts.save("online_out.mp3")
                os.system("start online_out.mp3" if os.name == "nt" else "open online_out.mp3")
            except Exception as e:
                print(f"Online TTS Error: {e}. Falling back to offline...")
                self._speak_offline(text)
        else:
            self._speak_offline(text)

    def _speak_offline(self, text):
        print("[TTS] Generating Local Offline Voice...")
        self.offline_engine.setProperty('rate', 140)
        self.offline_engine.say(text)
        self.offline_engine.runAndWait()
