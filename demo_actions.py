import time
import pyautogui
from voice_engine import VoiceEngine

ACTIONS = {
    "VOLUP":      lambda: [pyautogui.press("volumeup") for _ in range(5)],
    "VOLDOWN":    lambda: [pyautogui.press("volumedown") for _ in range(5)],
    "MUTE":       lambda: pyautogui.press("volumemute"),
    "PLAYPAUSE":  lambda: pyautogui.press("playpause"),
    "NEXT":       lambda: pyautogui.press("nexttrack"),
    "PREV":       lambda: pyautogui.press("prevtrack"),
    "SCROLLUP":   lambda: pyautogui.scroll(300),
    "SCROLLDOWN": lambda: pyautogui.scroll(-300),
    "CLICK":      lambda: pyautogui.click(),
}

def handle(cmd):
    print("[VOICE]", cmd)
    action = ACTIONS.get(cmd)
    if action:
        action()

voice = VoiceEngine(on_command=handle)
voice.start()
print("Demo running. Ctrl+C to quit.")
try:
    while True:
        time.sleep(0.2)
except KeyboardInterrupt:
    voice.stop()