
import pytesseract, os
from PIL import Image
from src.common.logging import audit

def ocr_image(image_path: str, lang: str="eng+fas", psm: int=3):
    if not os.path.exists(image_path):
        res={"ok":False,"error":"not_found","image_path":image_path}
        audit("ocr", {"image_path":image_path}, res); return res
    cfg = f"--psm {psm}"
    text = pytesseract.image_to_string(Image.open(image_path), lang=lang, config=cfg)
    res={"ok":True,"text":text}
    audit("ocr", {"image_path":image_path,"lang":lang}, {"ok":True,"chars":len(text)}); return res
