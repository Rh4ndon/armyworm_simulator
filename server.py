import http.server
import webbrowser
import threading

PORT = 8765

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # quiet

if __name__ == "__main__":
    print(f"🌾 Open your browser to: http://localhost:{PORT}")
    threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
