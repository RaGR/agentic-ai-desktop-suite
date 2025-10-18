
import os, subprocess
from src.common.logging import audit

def speak(text:str, voice_model_path:str=None, out_path:str=None):
    out_path = out_path or os.path.join(os.environ.get("AGENT_LOG_DIR", r"C:\Agent\logs"), "out.wav")
    piper = "piper.exe" if os.name=="nt" else "piper"
    ok=False
    try:
        if voice_model_path:
            cmd = [piper, "-m", voice_model_path, "-f", out_path, "-q"]
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            p.communicate(input=text, timeout=60)
            ok = (p.returncode==0 and os.path.exists(out_path))
    except Exception:
        ok=False
    if not ok and os.name=="nt":
        try:
            import win32com.client as w32
            spk = w32.Dispatch("SAPI.SpVoice"); spk.Speak(text); ok=True
        except Exception: ok=False
    res={"ok":ok,"out_path":out_path}
    audit("tts", {"text_len":len(text)}, res); return res
