import os

def calculate_bandwidth_savings(audio_path, text_string):
    if os.path.exists(audio_path):
        raw_audio_bytes = os.path.getsize(audio_path)
    else:
        raw_audio_bytes = 48000 * 2 * 3 

    text_bytes = len(text_string.encode('utf-8'))
    if text_bytes == 0: text_bytes = 1
        
    reduction = ((raw_audio_bytes - text_bytes) / raw_audio_bytes) * 100
    
    return {
        "audio_size_kb": round(raw_audio_bytes / 1024, 2),
        "text_size_kb": round(text_bytes / 1024, 4),
        "savings_percent": round(reduction, 2)
    }
