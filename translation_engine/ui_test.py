import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.hybrid_tts import HybridTTS
from src.link_sim import calculate_bandwidth_savings

# Initialize the primary application window base
root = tk.Tk()
root.title("NEXA VOICE - ISRO AI Transceiver Prototype")
root.geometry("850x600")
root.configure(bg="#1a1a1a")

# Active variables tracking
selected_lang = tk.StringVar(value="English")

# Trigger offline voice pipeline simulation
def process_transceiver_link():
    input_text = txt_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("System Warning", "Please input an active text payload vector first!")
        return
        
    lang = selected_lang.get()
    
    # Simulate a tactical translation fallback matrix
    if lang == "Hindi":
        translated_text = "निर्देशांक अल्फा पर आगे बढ़ें" # Direct offline Hindi translation mockup
    else:
        translated_text = input_text

    # Update Receiver side labels dynamically
    txt_payload.config(state="normal")
    txt_payload.delete("1.0", tk.END)
    txt_payload.insert(tk.END, f"📬 Packet Link Decoded: '{input_text}'")
    txt_payload.config(state="disabled")

    txt_translation.config(state="normal")
    txt_translation.delete("1.0", tk.END)
    txt_translation.insert(tk.END, translated_text)
    txt_translation.config(state="disabled")
    
    # Calculate simulation metrics directly via your repository tools
    metrics = calculate_bandwidth_savings("live_input.wav", input_text)
    lbl_metrics.config(text=f"📊 Low-Bitrate Channel Compression Rate: {metrics['savings_percent']}% Saved")

def play_received_audio():
    text_to_speak = txt_translation.get("1.0", tk.END).strip()
    if not text_to_speak or "Awaiting" in text_to_speak:
        return
    
    # Initialize your repository's native offline voice module
    try:
        tts = HybridTTS()
        tts.speak(text_to_speak, online_mode=False, target_lang=selected_lang.get())
    except Exception as e:
        messagebox.showerror("Audio Driver Error", f"Could not route audio: {e}")

# --- VISUAL INTERFACE STRUCTURE ---
lbl_title = tk.Label(root, text="📡 NEXA VOICE - ISRO AI Neural Transceiver", font=("Arial", 18, "bold"), fg="#ffffff", bg="#1a1a1a")
lbl_title.pack(pady=10)

# Sidebar Options Layout Strip
frame_settings = tk.Frame(root, bg="#2a2a2a", bd=2, relief="groove")
frame_settings.pack(fill="x", padx=15, pady=5)

lbl_lang = tk.Label(frame_settings, text="Active Command Language:", fg="#ffffff", bg="#2a2a2a", font=("Arial", 10))
lbl_lang.pack(side="left", padx=10, pady=5)

opt_lang = ttk.Combobox(frame_settings, textvariable=selected_lang, values=["English", "Hindi"], state="readonly", width=15)
opt_lang.pack(side="left", padx=5)

# Main Terminal Two-Column Frame Layout
main_frame = tk.Frame(root, bg="#1a1a1a")
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Column 1: Terminal Alpha (Sender)
col1 = tk.LabelFrame(main_frame, text=" 🎙️ Terminal Alpha (Sender Path) ", fg="#1f77b4", bg="#1a1a1a", font=("Arial", 12, "bold"))
col1.pack(side="left", fill="both", expand=True, padx=5)

lbl_input_hint = tk.Label(col1, text="Console Text Input Simulation Matrix:", fg="#ffffff", bg="#1a1a1a")
lbl_input_hint.pack(anchor="w", padx=10, pady=5)

txt_input = tk.Text(col1, height=6, bg="#2d2d2d", fg="#ffffff", insertbackground="white", font=("Arial", 11))
txt_input.pack(fill="x", padx=10, pady=5)
txt_input.insert(tk.END, "Proceed to coordinate Alpha")

btn_stream = tk.Button(col1, text="🚀 Stream Compressed Text over Bluetooth Socket", bg="#1f77b4", fg="white", font=("Arial", 10, "bold"), command=process_transceiver_link)
btn_stream.pack(fill="x", padx=10, pady=10)

lbl_metrics = tk.Label(col1, text="📊 Low-Bitrate Channel Compression Rate: 0.0% Saved", fg="#2ca02c", bg="#1a1a1a", font=("Arial", 11, "bold"))
lbl_metrics.pack(pady=10)

# Column 2: Terminal Beta (Receiver)
col2 = tk.LabelFrame(main_frame, text=" 🔊 Terminal Beta (Receiver Path) ", fg="#ff7f0e", bg="#1a1a1a", font=("Arial", 12, "bold"))
col2.pack(side="right", fill="both", expand=True, padx=5)

txt_payload = tk.Text(col2, height=4, bg="#222733", fg="#ff7f0e", font=("Arial", 11))
txt_payload.insert(tk.END, "Awaiting transmission packet streams...")
txt_payload.config(state="disabled")
txt_payload.pack(fill="x", padx=10, pady=5)

lbl_trans_hint = tk.Label(col2, text="🤖 Smart Multilingual Neural Translation Output:", fg="#ffffff", bg="#1a1a1a")
lbl_trans_hint.pack(anchor="w", padx=10, pady=5)

txt_translation = tk.Text(col2, height=4, bg="#1d2d24", fg="#2ca02c", font=("Arial", 11))
txt_translation.insert(tk.END, "Awaiting decoding link parameters...")
txt_translation.config(state="disabled")
txt_translation.pack(fill="x", padx=10, pady=5)

btn_audio = tk.Button(col2, text="🔊 Synthesize Neural Speech Playback", bg="#ff7f0e", fg="white", font=("Arial", 10, "bold"), command=play_received_audio)
btn_audio.pack(fill="x", padx=10, pady=15)

root.mainloop()
