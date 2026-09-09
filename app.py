import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wav
import pandas as pd
import os
import queue

st.set_page_config(page_title="SIH 173 - iTantra Transceiver", layout="wide")

st.title("📡 Project iTantra - ISRO AI Transceiver Dashboard")
st.subheader("Neural STT/TTS Link for Multilingual Space Radio Applications")

# Sidebar Configuration for Judges
st.sidebar.header("⚙️ Transceiver Settings")
network_mode = st.sidebar.radio("Select Processing Mode:", ["🌐 Online Mode (Fast Cloud APIs)", "🔒 Strict Offline Mode (Local AI)"])
is_online = "Online" in network_mode
selected_language = st.sidebar.selectbox("Select Target Language:", ["English", "Hindi", "Telugu", "Tamil"])

from src.hybrid_stt import HybridSTT
from src.hybrid_tts import HybridTTS
from src.link_sim import calculate_bandwidth_savings

@st.cache_resource
def load_engines():
    return HybridSTT(), HybridTTS()

stt_engine, tts_engine = load_engines()

col1, col2 = st.columns(2)

with col1:
    st.header("🎙️ Sender Terminal (Audio Input)")
    input_method = st.radio("Choose Input Method:", ["🔴 Live Microphone Recording", "📁 Upload a WAV Audio File"])
    audio_filename = "live_input.wav"

    if input_method == "🔴 Live Microphone Recording":
        st.write("### 🎤 Unlimited Live Recording Controller")
        
        # Audio storage initialization state
        if 'is_recording' not in st.session_state:
            st.session_state['is_recording'] = False
        if 'audio_queue' not in st.session_state:
            st.session_state['audio_queue'] = queue.Queue()
            
        fs = 16000  # 16kHz sampling rate required for AI acoustic models
        
        def audio_callback(indata, frames, time, status):
            """Tracks and appends continuous live microphone blocks dynamically."""
            st.session_state['audio_queue'].put(indata.copy())

        # Dual action toggle framework for premium UX feel
        if not st.session_state['is_recording']:
            if st.button("🔴 Start Recording Voice (Unlimited Time)", use_container_width=True):
                st.session_state['is_recording'] = True
                st.session_state['audio_queue'] = queue.Queue()  # Reset queue data structures
                st.rerun()
        else:
            st.warning("🎙️ System is actively listening... Speak now!")
            
            # Non-blocking continuous background sampler stream setup
            if 'stream' not in st.session_state:
                st.session_state['stream'] = sd.InputStream(samplerate=fs, channels=1, callback=audio_callback)
                st.session_state['stream'].start()
                
            if st.button("⏹️ Stop Recording & Process Audio Data", use_container_width=True):
                st.session_state['is_recording'] = False
                
                # Halt recording loops safely
                if 'stream' in st.session_state:
                    st.session_state['stream'].stop()
                    st.session_state['stream'].close()
                    del st.session_state['stream']
                    
                # Collect audio segments from background memory queue
                audio_data = []
                while not st.session_state['audio_queue'].empty():
                    audio_data.append(st.session_state['audio_queue'].get())
                
                if audio_data:
                    import numpy as np
                    final_audio = np.concatenate(audio_data, axis=0)
                    wav.write(audio_filename, fs, final_audio)
                    st.success("Recording caught and cached locally!")
                    
                    with st.spinner("Processing speech-to-text..."):
                        st.session_state['transcribed_text'] = stt_engine.transcribe(audio_filename, online_mode=is_online, target_lang=selected_language)
                else:
                    st.error("Error: No audio signal was detected from the microphone sample arrays.")
                st.rerun()
                
    else:
        uploaded_file = st.file_uploader("Upload a pre-recorded audio clip (.wav)", type=["wav"])
        if uploaded_file is not None:
            with open(audio_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Audio file verified and cached successfully!")
            
            if st.button("🔄 Process Uploaded Audio", use_container_width=True):
                with st.spinner("Processing speech-to-text..."):
                    st.session_state['transcribed_text'] = stt_engine.transcribe(audio_filename, online_mode=is_online, target_lang=selected_language)

    if 'transcribed_text' in st.session_state:
        st.text_area(f"Generated {selected_language} Text Packet Payload:", st.session_state['transcribed_text'])
        
        metrics = calculate_bandwidth_savings(audio_filename, st.session_state['transcribed_text'])
        st.metric(label="📊 Total Satellite Bandwidth Saved", value=f"{metrics['savings_percent']}%")
        
        st.write("### 📉 Payload Footprint Analysis")
        chart_data = pd.DataFrame({
            'Data Segment': ['Raw Voice Audio', 'Compressed Text Bytes'],
            'Size (KB)': [metrics['audio_size_kb'], metrics['text_size_kb']]
        })
        st.bar_chart(data=chart_data, x='Data Segment', y='Size (KB)', color='#2b5c8f')

with col2:
    st.header("🔊 Receiver Terminal (Audio Output)")
    if 'transcribed_text' in st.session_state:
        st.info(f"Incoming Text Stream Received: '{st.session_state['transcribed_text']}'")
        
        if st.button("🟢 Synthesize & Play Audio Locally", use_container_width=True):
            with st.spinner("Generating audio waves..."):
                tts_engine.speak(st.session_state['transcribed_text'], online_mode=is_online)
                st.success("Audio playback execution completed.")
    else:
        st.write("Waiting for data transmission packet from Sender Terminal...")
