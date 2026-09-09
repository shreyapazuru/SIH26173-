import os
import speech_recognition as sr
from faster_whisper import WhisperModel

class HybridSTT:
    def __init__(self, model_size="tiny"):
        self.model_size = model_size
        self.offline_model = None

    def transcribe(self, audio_path, online_mode=False):
        if not os.path.exists(audio_path):
            return "Error: Local audio file missing."

        if online_mode:
            print("[STT] Using Online Google API...")
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language="en-IN")
            except Exception as e:
                return f"Online STT Failed (Check Internet): {e}"
        else:
            print("[STT] Using Local Offline Faster-Whisper...")
            if self.offline_model is None:
                self.offline_model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            
            segments, info = self.offline_model.transcribe(audio_path, beam_size=3)
            return "".join([segment.text for segment in segments]).strip()
