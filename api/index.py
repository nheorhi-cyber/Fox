import asyncio
from PIL import Image
from vercel import Response

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

async def handler(request):
    async def generate():
        while True:
            for frame in frames:
                yield '\033[2J\033[H' + frame
                await asyncio.sleep(1 / FPS)
    
    return Response(generate(), headers={'Content-Type': 'text/plain'})