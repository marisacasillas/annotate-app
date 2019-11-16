"""
Ensure that the Annotation server is running, then launch a Chrome tab,
directing it to the application login page. We test whether or not the server
is running by trying to connect to it as a client. We use the "start" command
to launch processes in the background (after changing to the relevant working
directory), and we use "pythonw" to launch a python process that doesn't come
with an associated python window.
"""

import socket
import subprocess
import time

server_running = True
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8080))
    s.close()
except socket.error:
    server_running = False

if not server_running:
    subprocess.call([
        'start',
        'Annotate Server',
        '/D', r'C:\Users\terminalpc\Documents\Annotate',
        'pythonw',
        'app.py'
    ], shell=True)
    time.sleep(0.5)

subprocess.call([
    'start',
    'chrome.exe',
    'http://127.0.0.1:8080/login'
], shell=True)
