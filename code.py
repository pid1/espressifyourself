import wifi
import os
from adafruit_magtag.magtag import MagTag
import socketpool
from adafruit_httpserver import Server, Request, Response

magtag = MagTag()

wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    hello world!
    <br><br>
    this is a development server running on an ESP32-S2 via CircuitPython
    <br><br>
    brought to you by <a href="https://pid1.space">pid1</a>
    <br><br>
    <img src="fastweb.gif" alt="GIF explaining that the website is fast">
    </html>
    """
    return html

@server.route("/")
def base(request: Request):
    return Response(request, f"{webpage()}", content_type='text/html')

@server.route("/static")
def base(request: Request):
    return Response(request, f"{webpage()}", content_type='text/html')

server.start()

while True:
    try:
        server.poll()  # Process incoming requests
    except Exception as e:
        print("Error:", e)

