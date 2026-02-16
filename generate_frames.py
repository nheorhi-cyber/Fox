import json
from PIL import Image

GIF_PATH = "Fox.gif"
WIDTH = 80

def img_to_ascii(img, w):
    h = int(img.height / img.width * w * 0.55)
    img = img.resize((w, h)).convert('L')
    pix = img.getdata()
    chars = "@%#*+=-:. "[::-1]
    out = ""
    for i, p in enumerate(pix):
        if i % w == 0 and i: out += "\n"
        out += chars[min(p * len(chars) // 256, len(chars)-1)]
    return out

frames = []
gif = Image.open(GIF_PATH)
try:
    while True:
        gif.seek(len(frames))
        frames.append(img_to_ascii(gif.convert('RGB'), WIDTH))
except EOFError:
    pass

with open('frames.json', 'w') as f:
    json.dump(frames, f)

print(f"Saved {len(frames)} frames to frames.json")