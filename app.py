from flask import Flask, Response
from PIL import Image
import time
import json
import os

app = Flask(__name__)

GIF_PATH = "Fox.gif"
WIDTH = 80
FPS = 10

frames = []

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

# Load frames
gif = Image.open(GIF_PATH)
try:
    while True:
        gif.seek(len(frames))
        frames.append(img_to_ascii(gif.convert('RGB'), WIDTH))
except EOFError:
    pass

def generate():
    while True:
        for frame in frames:
            yield '\033[2J\033[H' + frame
            time.sleep(1 / FPS)

@app.route('/')
def index():
    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)