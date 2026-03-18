import http.server
import socketserver
import webbrowser
import threading
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Microsoft Course Hub running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()

if __name__ == "__main__":
    # Change to root directory
    os.chdir(DIRECTORY)
    
    # Start server in a separate thread
    threading.Thread(target=start_server, daemon=True).start()
    
    # Open the browser
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    
    print("\n--- NFS Microsoft Course Hub ---")
    print(f"Serving files from: {DIRECTORY}")
    print(f"URL: http://localhost:{PORT}/index.html")
    print("------------------------------------\n")
    
    try:
        # Keep main thread alive
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down hub...")
        sys.exit(0)
