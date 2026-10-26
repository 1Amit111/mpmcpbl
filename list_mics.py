import sounddevice as sd
print(sd.query_devices())
print("Default input:", sd.default.device[0])