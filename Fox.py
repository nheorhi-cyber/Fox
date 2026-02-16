import http.server, socketserver, time
from PIL import Image

GIF_PATH = "Fox.gif"
WIDTH = 80
FPS = 10
PORT = 9091

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

gif = Image.open(GIF_PATH)
try:
    while True:
        gif.seek(len(frames))
        frames.append(img_to_ascii(gif.convert('RGB'), WIDTH))
except EOFError:
    pass
print(f"Loaded {len(frames)} frames")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        while True:
            for f in frames:
                self.wfile.write(b'\033[2J\033[H' + f.encode())
                time.sleep(1/FPS)
    def log_message(self, *args): pass

httpd = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
print(f"Server on port {PORT}, connect: curl http://<IP>:{PORT}")
httpd.serve_forever()