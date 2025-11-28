#!/usr/bin/env python3
"""Simple HTTP server to serve demo pages"""

import http.server
import socketserver
import threading
import time
import os

class DemoServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.thread = None
        
    def start(self):
        """Start the server in a background thread"""
        os.chdir('/Users/aarij.hussaan/development/ollama_tester')
        
        handler = http.server.SimpleHTTPRequestHandler
        self.server = socketserver.TCPServer(("", self.port), handler)
        
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        print(f"🌐 Demo server started at http://localhost:{self.port}")
        time.sleep(1)  # Give server time to start
        
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 Demo server stopped")

if __name__ == "__main__":
    server = DemoServer()
    server.start()
    
    try:
        print("Server running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()