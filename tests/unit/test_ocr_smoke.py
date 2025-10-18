
from PIL import Image, ImageDraw
from src.tools.ocr import ocr_image
import tempfile, os
def test_ocr_smoke():
    img=Image.new("RGB",(400,100),"white"); d=ImageDraw.Draw(img); d.text((10,40),"Hello World!", fill="black")
    p=os.path.join(tempfile.gettempdir(),"ocr_test.png"); img.save(p)
    r=ocr_image(p, "eng", 6)
    assert "Hello" in r.get("text","")
