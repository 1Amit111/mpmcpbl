import time
from voice_engine import VoiceEngine

def handle(cmd):
    print("Controller got:", cmd)

def on_error(reason):
    print("Controller got error: ERR:" + reason)

voice = VoiceEngine(on_command=handle, on_error=on_error)
voice.start()

try:
    while True:
        print("--- VOICE mode ON for 15 s: say commands ---")
        voice.enabled = True
        time.sleep(15)
        print("--- VOICE mode OFF for 10 s: commands should be ignored ---")
        voice.enabled = False
        time.sleep(10)
except KeyboardInterrupt:
    voice.stop()