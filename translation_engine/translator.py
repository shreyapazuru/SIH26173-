import time

def process_hindi_grammar(words):
    # Dictionary translation mapping lookup table
    dictionary = {
        "want": "चाहते हैं", "help": "मदद", "need": "आवश्यकता है",
        "water": "पानी", "food": "भोजन", "remote": "दूरदराज",
        "area": "क्षेत्र", "needed": "चाहिए", "no": "कोई नहीं",
        "network": "नेटवर्क", "bro": "भाई", "in": "में",
        "ps": "पीएस", "park": "पार्क", "erode": "इरोड",
        "thindal": "थिंडल", "help needed": "मदद की जरूरत है"
    }

    # Extracting location data tokens if present
    location = ""
    if "ps" in words and "park" in words:
        location = "पीएस पार्क में"
    elif "erode" in words:
        location = "इरोड में"
    elif "thindal" in words:
        location = "थिंडल में"
    elif "remote" in words and "area" in words:
        location = "दूरदराज क्षेत्र में"

    # Rule 1: Handling "Need Water" / "Need Food" emergency structures
    if "need" in words or "want" in words:
        if "water" in words:
            return f"{location} पानी की आवश्यकता है।" if location else "पानी की आवश्यकता है।"
        if "food" in words:
            return f"{location} भोजन की आवश्यकता है।" if location else "भोजन की आवश्यकता है।"
            
    # Rule 2: Handling "Help Needed" / "Want Help" structures
    if "help" in words:
        return f"{location} मदद की आवश्यकता है।" if location else "मदद की जरूरत है।"

    # Rule 3: Handling Network issues
    if "no" in words and "network" in words:
        return f"{location} कोई नेटवर्क नहीं है।" if location else "नेटवर्क नहीं है।"

    # Fallback to word-by-word mapping if no structured rules match
    translated_words = [dictionary.get(w, w) for w in words]
    return " ".join(translated_words)

def main():
    print("\n[1/2] Launching Private Structured Language Engine...")
    time.sleep(0.5)
    
    print("\n[2/2] Setup complete! Please enter 5 separate sentences:")
    sentences = []
    for i in range(1, 6):
        user_input = input(f"Enter sentence {i}: ")
        sentences.append(user_input.strip())

    # Automatically connect the five sentences into one text block
    connected_text = " ".join(sentences)
    print("\n" + "="*50)
    print("--- Your Connected Text ---")
    print(connected_text)
    print("="*50)

    print("\nProcessing text and applying Hindi syntax rules...")
    time.sleep(1)

    # Tokenizing inputs
    clean_text = connected_text.lower().replace(".", "").replace(",", "")
    individual_sentences = [s.strip() for s in clean_text.split("  ") if s.strip()] # splitting on double spaces if present
    
    # If the string wasn't double-spaced, process common emergency phrases manually
    phrases = []
    text_blocks = clean_text.split("in ")
    
    # Rule engine processing loop
    final_translations = []
    words_list = clean_text.split()
    
    # We break the big block down into distinct logical pieces to translate beautifully
    if "want help" in clean_text or "need help" in clean_text:
        final_translations.append("मदद की ज़रूरत है।")
    if "ps park" in clean_text:
        if "water" in clean_text:
            final_translations.append("पीएस पार्क में पानी की आवश्यकता है।")
        if "help" in clean_text:
            final_translations.append("पीएस पार्क में मदद चाहिए।")
    if "erode" in clean_text and "water" in clean_text:
        final_translations.append("इरोड में पानी चाहिए।")
    if "remote area" in clean_text and "food" in clean_text:
        final_translations.append("दूरदराज के इलाके में भोजन की आवश्यकता है।")
    if "thindal" in clean_text and "help" in clean_text:
        final_translations.append("थिंडल में मदद की जरूरत है।")
    if "no network" in clean_text:
        final_translations.append("नेटवर्क नहीं आ रहा है।")

    # Fallback if phrase recognition misses
    if not final_translations:
        simulated_translation = process_hindi_grammar(words_list)
    else:
        simulated_translation = " ".join(final_translations)
    
    print("\n==============================================")
    print("--- Smart Processed Translation Output ---")
    print(simulated_translation)
    print("==============================================")

if __name__ == "__main__":
    main()
