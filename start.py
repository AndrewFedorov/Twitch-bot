from main import main
from http.server import HTTPServer, CGIHTTPRequestHandler
import threading


def startsite():
    server_address = ("localhost", 8000)
    #CGIHTTPRequestHandler.cgi_directories = "/scripts"
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=startsite).start()
main()