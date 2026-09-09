import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wav
import os
from src.hybrid_stt import HybridSTT
from src.hybrid_tts import HybridTTS
from src.link_sim import calculate_bandwidth_savings

st.set_page_config(page_title="SIH 173 - iTantra Transceiver", layout="wide")

st.title("📡 Project iTantra - ISRO AI Transceiver Dashboard")
st.subheader("Neural STT/TTS Link for Low-Bitrate Space Radio Applications")

# Add the network configuration switch right at the top
st.sidebar.header("⚙️ Network Settings")
network_mode = st.sidebar.radio("Select Processing Mode:", ["🌐 Online Mode (Fast Cloud APIs)", "🔒 Strict Offline Mode (Local AI)"])
is_online = "Online" in network_mode

@st.cache_resource
def load_engines():
    return HybridSTT(), HybridTTS()

stt_engine, tts_engine = load_engines()

col1, col2 = st.columns(2)

with col1:
    st.header("🎙️ Sender Terminal (Audio Input)")
    
    # Let the user choose between live recording or uploading an audio file
    input_method = st.radio("Choose Input Method:", ["🔴 Live Microphone Recording", "📁 Upload a WAV Audio File"])
    
    audio_filename = "live_input.wav"

    if input_method == "🔴 Live Microphone Recording":
        duration = st.slider("Recording Duration (seconds)", 2, 10, 4)
        if st.button("🔴 Start Recording Live Voice", use_container_width=True):
            try:
                fs = 16000
                st.info("Recording... Speak into your mic now!")
                recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
                sd.wait()
                wav.write(audio_filename, fs, recording)
                st.success("Recording saved locally!")
                
                with st.spinner("Processing speech-to-text..."):
                    st.session_state['transcribed_text'] = stt_engine.transcribe(audio_filename, online_mode=is_online)
            except Exception as e:
                st.error(f"Microphone Error: {e}. Please use the 'Upload a WAV Audio File' option below or verify your system mic.")
                
    else:
        uploaded_file = st.file_uploader("Upload a pre-recorded audio clip (.wav)", type=["wav"])
        if uploaded_file is not None:
            with open(audio_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Audio file uploaded successfully!")
            
            if st.button("🔄 Process Uploaded Audio", use_container_width=True):
                with st.spinner("Processing speech-to-text..."):
                    st.session_state['transcribed_text'] = stt_engine.transcribe(audio_filename, online_mode=is_online)

    if 'transcribed_text' in st.session_state:
        st.text_area("Generated Text Packet Payload:", st.session_state['transcribed_text'])
        
        metrics = calculate_bandwidth_savings(audio_filename, st.session_state['transcribed_text'])
        st.metric(label="📊 Bandwidth Saved for ISRO Satellite Link", value=f"{metrics['savings_percent']}%")
        st.write(f"📁 Raw Voice File Size: **{metrics['audio_size_kb']} KB**")
        st.write(f"📄 Compressed Text Packet Size: **{metrics['text_size_kb']} KB**")

with col2:
    st.header("🔊 Receiver Terminal (Audio Output)")
    
    if 'transcribed_text' in st.session_state:
        st.info(f"Incoming Text Stream Received: '{st.session_state['transcribed_text']}'")
        
        if st.button("🟢 Synthesize & Play Audio", use_container_width=True):
            with st.spinner("Generating audio waves..."):
                tts_engine.speak(st.session_state['transcribed_text'], online_mode=is_online)
                st.success("Audio playback execution completed.")
    else:
        st.write("Waiting for data transmission packet from Sender Terminal...")
