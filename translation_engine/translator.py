import time

def main():
    print("\n[1/2] Launching Private Embedded Language Engine...")
    time.sleep(1)
    
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

    print("\nProcessing text and mapping translations...")
    time.sleep(1)

    # Dictionary translation mapping lookup table
    dictionary = {
        "hello": "नमस्ते", 
        "world": "दुनिया", 
        "ai": "कृत्रिम बुद्धिमत्ता",
        "project": "परियोजना", 
        "success": "सफलता", 
        "system": "प्रणाली",
        "good": "अच्छा", 
        "morning": "सुबह", 
        "thank": "धन्यवाद", 
        "you": "आपको"
    }
    
    words = connected_text.lower().replace(".", "").replace(",", "").split()
    translated_words = [dictionary.get(w, w) for w in words]
    simulated_translation = " ".join(translated_words)
    
    print("\n==============================================")
    print("--- Processed Translation Output ---")
    print(simulated_translation)
    print("==============================================")

if __name__ == "__main__":
    main()
