import keyboard
import pyperclip
import time
from config import snippets, banner

last_execution_time = 0
debounce_interval = 0.3  # 300 milliseconds
close = "ctrl+`"

def replace_snippet():
    global last_execution_time
    current_time = time.time()
    
    if current_time - last_execution_time < debounce_interval:
        return  # Ignore if called too soon after last execution
    
    last_execution_time = current_time
    
    time.sleep(0.1)  # Give the system time to process the key press
    word = get_last_word()
    if word in snippets:
        # Delete the trigger word
        for _ in range(len(word)):
            keyboard.send('backspace')
        time.sleep(0.1)  # Ensure the word is deleted
        
        # Type out the snippet without leading space
        expanded_text = snippets[word].lstrip()  # Remove leading whitespace
        keyboard.write(expanded_text)
    
    # Explicitly release Ctrl and Space keys
    keyboard.release('ctrl')
    keyboard.release('space')

def get_last_word():
    # Use clipboard to get the last word typed
    original_clipboard = pyperclip.paste()  # Save original clipboard content
    keyboard.send('ctrl+shift+left')  # Select the last word
    keyboard.send('ctrl+c')           # Copy the selection to clipboard
    time.sleep(0.1)                   # Wait for clipboard to update
    word = pyperclip.paste().strip()  # Remove any leading/trailing whitespace
    pyperclip.copy(original_clipboard)  # Restore original clipboard content
    keyboard.send('right')            # Move cursor back to end
    return word

# Register a listener for Ctrl + Space to detect end of word
keyboard.add_hotkey('ctrl+space', replace_snippet, suppress=True, trigger_on_release=True)

print(banner)
print(f"Text expander is running... Press {close} to stop.")
keyboard.wait(close)

# Ensure all keys are released when exiting
keyboard.release('ctrl')
keyboard.release('space')