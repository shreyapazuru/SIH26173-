import pyttsx3
from gtts import gTTS
import os

class HybridTTS:
    def __init__(self):
        self.offline_engine = pyttsx3.init()
        self.setup_regional_voices()

    def setup_regional_voices(self):
        """Scans the host laptop for installed regional language voice packs."""
        self.voices = self.offline_engine.getProperty('voices')
        self.lang_voice_id = None
        
        # Look for Indian accent or regional voice packs installed on Windows/Mac
        for voice in self.voices:
            if "india" in voice.name.lower() or "hindi" in voice.name.lower() or "hi" in voice.id.lower():
                self.lang_voice_id = voice.id
                break

    def speak(self, text, online_mode=False, target_lang="English"):
        if not text:
            return

        # Map display choices to standard ISO language codes
        lang_codes = {"English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta"}
        lang_code = lang_codes.get(target_lang, "en")

        if online_mode:
            print(f"[TTS] Generating Online Google Voice for {target_lang}...")
            try:
                # Generates natural regional voice streams over the network
                tts = gTTS(text=text, lang=lang_code, tld='co.in')
                tts.save("online_out.mp3")
                
                # Command execution layers optimized for seamless Windows/Mac audio routing
                if os.name == "nt":
                    os.system("start /min "" online_out.mp3")
                else:
                    os.system("open online_out.mp3")
            except Exception as e:
                print(f"Online TTS Error: {e}. Switching back to offline native layer...")
                self._speak_offline(text)
        else:
            self._speak_offline(text)

    def _speak_offline(self, text):
        print("[TTS] Generating Local Offline System Voice...")
        if self.lang_voice_id:
            self.offline_engine.setProperty('voice', self.lang_voice_id)
        
        self.offline_engine.setProperty('rate', 140)
        self.offline_engine.say(text)
        self.offline_engine.runAndWait()

