"""
This module simulates a client that opens a TCP connection to the server, makes a web
request, and closes the connection after 1 second.

This is to verify how the ASGI server and the web application handle this kind of
situations.
"""
import os
import requests
from requests.exceptions import ReadTimeout


def fire_and_close():
    if os.environ.get("WAIT") == "1":
        response = requests.get("http://localhost:8000/")
        print("Received:", response.text)
    else:
        try:
            requests.get("http://localhost:8000/", timeout=1)
        except ReadTimeout:
            print("Closed the connection 💣")


fire_and_close()
