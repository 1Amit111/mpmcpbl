import json, queue, os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "models", "vosk-model-small-en-us-0.15")
SAMPLE_RATE = 16000

q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    q.put(bytes(indata))

print("Loading model...")
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, SAMPLE_RATE)

print("Listening... say something (Ctrl+C to stop)")
with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000,
                       dtype="int16", channels=1, callback=audio_callback):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if text:
                print("Heard:", text)