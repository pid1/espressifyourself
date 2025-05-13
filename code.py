import wifi
import os
from adafruit_magtag.magtag import MagTag
import socketpool
from adafruit_httpserver import Server, Request, Response

magtag = MagTag()

wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/")
def base(request: Request):
    try:
        with open("/static/index.html", "r") as file:
            html_content = file.read()
        return Response(request, html_content, content_type='text/html')
    except Exception as e:
        return Response(request, f"Error loading file: {e}", content_type='text/plain')

server.start()

while True:
    try:
        server.poll()  # Process incoming requests
    except Exception as e:
        print("Error:", e)
