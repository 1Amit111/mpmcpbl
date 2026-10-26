import json, queue, os, time, subprocess, ctypes
from urllib.parse import quote_plus
import sounddevice as sd
import pyautogui
from vosk import Model, KaldiRecognizer, SetLogLevel
from voice_engine import LOOKUP        # reuse your command phrases

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "models", "vosk-model-small-en-us-0.15")
SAMPLE_RATE = 16000
COOLDOWN = 0.5

def search_chrome(query):
    url = "https://www.google.com/search?q=" + quote_plus(query)
    subprocess.Popen(f'start chrome "{url}"', shell=True)

ACTIONS = {
    "VOLUP":        lambda: [pyautogui.press("volumeup") for _ in range(5)],
    "VOLDOWN":      lambda: [pyautogui.press("volumedown") for _ in range(5)],
    "MUTE":         lambda: pyautogui.press("volumemute"),
    "PLAYPAUSE":    lambda: pyautogui.press("playpause"),
    "NEXT":         lambda: pyautogui.press("nexttrack"),
    "PREV":         lambda: pyautogui.press("prevtrack"),
    "SCROLLUP":     lambda: pyautogui.scroll(300),
    "SCROLLDOWN":   lambda: pyautogui.scroll(-300),
    "CLICK":        lambda: pyautogui.click(),
    "ZOOMIN":       lambda: pyautogui.hotkey("ctrl", "="),
    "ZOOMOUT":      lambda: pyautogui.hotkey("ctrl", "-"),
    "OPEN_CHROME":  lambda: subprocess.Popen("start chrome", shell=True),
    "OPEN_NOTEPAD": lambda: subprocess.Popen("notepad"),
    "SCREENSHOT":   lambda: pyautogui.screenshot("screenshot.png"),
    "LOCK":         lambda: ctypes.windll.user32.LockWorkStation(),
}

SEARCH_WORDS = ("search for ", "search ", "google ")

q = queue.Queue()
last = {}

def audio_cb(indata, frames, t, status):
    q.put(bytes(indata))

def handle(text):
    print("   (heard:", text + ")", flush=True)
    # 1) search request: "search for <anything>"
    for w in SEARCH_WORDS:
        if text.startswith(w) and len(text) > len(w):
            query = text[len(w):]
            print("[VOICE] SEARCH:", query, flush=True)
            search_chrome(query)
            return
    # 2) normal command
    cmd = LOOKUP.get(text)
    if not cmd:
        return
    now = time.time()
    if now - last.get(cmd, 0) < COOLDOWN:
        return
    last[cmd] = now
    print("[VOICE]", cmd, flush=True)
    action = ACTIONS.get(cmd)
    if action:
        action()

SetLogLevel(-1)
print("Loading model...")
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, SAMPLE_RATE)      # no grammar = hears any words
print("Ready. Say 'search for ...' or a command. Ctrl+C to quit.")

with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000,
                       dtype="int16", channels=1, callback=audio_cb):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if text:
                handle(text)