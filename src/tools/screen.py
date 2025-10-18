
import os
import mss
from PIL import Image
from src.common.logging import audit

def capture(mode: str="full", region=None, active_window=False):
    with mss.mss() as sct:
        if mode=="region" and region:
            bbox = {"left":region[0], "top":region[1], "width":region[2], "height":region[3]}
            shot = sct.grab(bbox)
        else:
            mon = sct.monitors[1]
            shot = sct.grab(mon)
    img = Image.frombytes("RGB", shot.size, shot.rgb)
    path = os.path.join(os.environ.get("AGENT_LOG_DIR", r"C:\Agent\logs"), "screen.png")
    img.save(path)
    res={"ok":True,"image_path":path,"size":img.size}
    audit("screen.capture", {"mode":mode,"region":region}, res); return res
