#!/usr/bin/env python3
"""
🔥 Screen Share Server - Simple HTTP + WebSocket Relay
Usage: python server.py
Access: http://YOUR-IP:8000/screenshare.html
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os
import urllib.parse
from http import HTTPStatus

PORT = 8000
ROOMS = {}  # Simple room storage

class ScreenShareHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/screenshare.html'
        
        # Serve static files
        super().do_GET()
    
    def end_headers(self):
        # CORS for all origins
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_POST(self):
        if self.path == '/ws':
            # WebSocket relay endpoint
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = post_data.decode('utf-8')
            
            # Broadcast to room
            try:
                msg = eval(data)  # Simple JSON-like parsing
                room = msg.get('room') or msg.get('join')
                if room:
                    if room not in ROOMS:
                        ROOMS[room] = []
                    ROOMS[room].append(self)
                    # Broadcast to room members
                    for client in ROOMS.get(room, []):
                        client.send(data.encode())
            except:
                pass
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def open_browser():
    time.sleep(2)
    webbrowser.open(f'http://localhost:{PORT}')
    print(f"\n🚀 OPENED: http://localhost:{PORT}/screenshare.html")
    print(f"📱 SENDER: http://localhost:{PORT}/screenshare.html")
    print(f"📺 RECEIVER: http://localhost:{PORT}/screenshare.html")

def print_ip():
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"🌐 LOCAL:   http://localhost:{PORT}")
    print(f"🌐 NETWORK: http://{local_ip}:{PORT}")
    print(f"📱 PHONE:   http://{local_ip}:{PORT}/screenshare.html")

if __name__ == "__main__":
    print("🔥 Screen Share Server Starting...")
    print("📁 Files:", os.listdir('.'))
    
    with socketserver.TCPServer(("", PORT), ScreenShareHandler) as httpd:
        print_ip()
        
        # Auto-open browser
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print(f"\n🎉 Server running on port {PORT} (Ctrl+C to stop)")
        print("📖 Usage:")
        print("   1. TAB1: Sender → START → Copy Room ID")
        print("   2. TAB2: Receiver → Paste Room ID → CONNECT")
        print("\n🌐 Share with phone: http://YOUR-IP:8000/screenshare.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")