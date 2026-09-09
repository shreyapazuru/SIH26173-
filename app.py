import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NEXA VOICE - Test", layout="wide")

# Updated Branding
st.title("📡 NEXA VOICE - ISRO Transceiver Prototype")
st.subheader("Challenge ID: 26173 | Indian Multilingual Audio Neural Link")

from src.hybrid_stt import HybridSTT
from src.hybrid_tts import HybridTTS
from src.link_sim import calculate_bandwidth_savings

@st.cache_resource
def load_engines():
    return HybridSTT(), HybridTTS()

stt_engine, tts_engine = load_engines()

# Network Settings Sidebar
st.sidebar.header("⚙️ NEXA VOICE Controls")
network_mode = st.sidebar.radio("Processing Engine:", ["🌐 Online Mode (Fast Cloud APIs)", "🔒 Strict Offline Mode (Local AI)"])
is_online = "Online" in network_mode
selected_language = st.sidebar.selectbox("Active Language:", ["English", "Hindi", "Telugu", "Tamil"])

col1, col2 = st.columns(2)

with col1:
    st.header("🎙️ Terminal Alpha (Sender)")
    
    # PREMIUM MOBILE UX ENGINE: Uses the phone's native microphone directly!
    audio_value = st.audio_input("🔴 Press the Mic button to Record Voice") #
    
    audio_filename = "mobile_input.wav"

    if audio_value:
        # Save the phone's recorded mic bytes to a local wav file
        with open(audio_filename, "wb") as f:
            f.write(audio_value.getbuffer())
        st.success("Voice sample successfully captured from your phone!")
        
        if st.button("🚀 TRANSMIT PACKET OVER SATELLITE SIMULATOR", use_container_width=True):
            with st.spinner("Processing speech-to-text..."):
                st.session_state['transcribed_text'] = stt_engine.transcribe(audio_filename, online_mode=is_online, target_lang=selected_language)

    if 'transcribed_text' in st.session_state:
        st.text_area("🔒 Outgoing Text Payload:", st.session_state['transcribed_text'])
        
        # Bandwidth Calculation Metric
        metrics = calculate_bandwidth_savings(audio_filename, st.session_state['transcribed_text'])
        st.metric(label="📊 Total Satellite Bandwidth Saved", value=f"{metrics['savings_percent']}%")
        
        # Beautiful Interactive Payload Analysis Bar Chart
        st.write("### 📉 Payload Footprint Analysis")
        chart_data = pd.DataFrame({
            'Data Segment': ['Raw Voice Audio', 'Compressed Text Bytes'],
            'Size (KB)': [metrics['audio_size_kb'], metrics['text_size_kb']]
        })
        st.bar_chart(data=chart_data, x='Data Segment', y='Size (KB)', color='#2b5c8f')

with col2:
    st.header("🔊 Terminal Beta (Receiver)")
    if 'transcribed_text' in st.session_state:
        st.info(f"Incoming Text Stream Received: '{st.session_state['transcribed_text']}'")
        
        if st.button("🟢 Synthesize & Play Audio on Phone Speaker", use_container_width=True):
            with st.spinner("Generating voice waves..."):
                tts_engine.speak(st.session_state['transcribed_text'], online_mode=is_online, target_lang=selected_language)
                st.success("Audio playback executed.")
    else:
        st.write("Awaiting asynchronous handshake data packets from peer device...")
