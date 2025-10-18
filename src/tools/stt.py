
import os, tempfile, sounddevice as sd, soundfile as sf
from faster_whisper import WhisperModel
from src.common.logging import audit

_model_cache = {}
def _get_model(size="base", device="cpu", compute_type="int8"):
    key=(size,device,compute_type)
    if key not in _model_cache:
        _model_cache[key]=WhisperModel(size, device=device, compute_type=compute_type)
    return _model_cache[key]

def record_to_wav(seconds=6, samplerate=16000, channels=1):
    audio = sd.rec(int(seconds*samplerate), samplerate=samplerate, channels=channels, dtype='float32')
    sd.wait()
    fd, path = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    sf.write(path, audio, samplerate)
    return path

def transcribe(audio_path:str=None, size="base", language="en"):
    if not audio_path: audio_path = record_to_wav()
    model = _get_model(size=size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, language=language, vad_filter=True, beam_size=1)
    text = " ".join([s.text.strip() for s in segments])
    res={"ok":True,"text":text,"language":language}
    audit("stt", {"audio_path":audio_path,"size":size,"lang":language}, {"ok":True,"chars":len(text)}); return res
