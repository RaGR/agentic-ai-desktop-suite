
import time, requests, keyboard, tempfile, os
import sounddevice as sd, soundfile as sf

API="http://127.0.0.1:8088"
PTT="ctrl+space"; SC="ctrl+alt+s"

def record(seconds=6, sr=16000):
    audio = sd.rec(int(seconds*sr), samplerate=sr, channels=1, dtype='float32'); sd.wait()
    fd, path = tempfile.mkstemp(suffix=".wav"); os.close(fd); sf.write(path, audio, sr); return path

def on_ptt():
    print("[PTT] Recording…"); wav=record()
    print("[PTT] Transcribing…"); stt=requests.post(f"{API}/tools/stt", json={"audio_path":wav}).json()
    print("[STT]", stt.get("text"))
    res=requests.post(f"{API}/chat", json={"text":stt.get("text","")}).json()
    print("[CHAT]", res.get("text","(no text)"))
    requests.post(f"{API}/tools/tts", json={"text":res.get("text","")})

def on_screen():
    sc=requests.post(f"{API}/tools/screen/capture", json={"mode":"full"}).json()
    o=requests.post(f"{API}/tools/ocr", json={"image_path":sc["image_path"]}).json()
    print("[OCR]\n", o.get("text","")[:400])

def main():
    keyboard.add_hotkey(PTT, on_ptt)
    keyboard.add_hotkey(SC, on_screen)
    print(f"Hotkeys ready: PTT={PTT}, SCREEN={SC}")
    while True: time.sleep(1)

if __name__=="__main__": main()
