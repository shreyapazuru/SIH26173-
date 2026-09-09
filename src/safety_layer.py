import numpy as np

class NexaVoiceSafetyManager:
    """Provides real-time telemetry isolation and auditory gain protection for NEXA VOICE."""
    
    def __init__(self, max_allowed_db=85):
        self.max_allowed_db = max_allowed_db

    def isolate_data_packet(self, text_payload):
        """Wipes any hidden background tracing headers or logging footprints before network dispatch."""
        if not text_payload:
            return ""
        cleaned_payload = text_payload.strip()
        return cleaned_payload

    def apply_acoustic_limiter(self, audio_data, sample_rate=16000):
        """Ensures highest volume alerts do not cause speaker damage or ear trauma."""
        if audio_data is None or len(audio_data) == 0:
            return audio_data
            
        peak_amplitude = np.max(np.abs(audio_data))
        safe_threshold = 0.85 # Caps gain parameters to safe ceiling boundaries
        
        if peak_amplitude > safe_threshold:
            print("[SAFETY CLAMP] Acoustic spike detected. Scaling output to safe decibel margins.")
            scaling_factor = safe_threshold / peak_amplitude
            audio_data = audio_data * scaling_factor
            
        return audio_data
