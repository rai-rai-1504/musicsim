"""
Run the RapSim Mobile UI Preview server.
Serves the 9:16 neomorphic mobile interface at http://127.0.0.1:8080
"""

import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

# Configure console utf-8 encoding for Windows compatibility
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ROOT_DIR = Path(__file__).resolve().parent
UI_DIR = ROOT_DIR / "rapsim-mobile-ui"
DEFAULT_PORT = 8080


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def end_headers(self):
        # Disable caching during development so UI tweaks show immediately
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Cleaner console logs
        sys.stdout.write(f"[RapSim Mobile UI] {args[0]} - {args[1]}\n")
        sys.stdout.flush()


def run_server(port=DEFAULT_PORT):
    os.chdir(str(UI_DIR))
    http.server.ThreadingHTTPServer.allow_reuse_address = True

    for attempt_port in range(port, port + 10):
        try:
            httpd = http.server.ThreadingHTTPServer(("127.0.0.1", attempt_port), CustomHTTPRequestHandler)
            httpd.daemon_threads = True
            url = f"http://127.0.0.1:{attempt_port}"
            print("=" * 60)
            print("[RapSim] Mobile UI (9:16 Neomorphic Preview) is live!")
            print(f"[RapSim] Local URL: {url}")
            print(f"[RapSim] Orientation: 9:16 Mobile Simulator")
            print("=" * 60)
            print("Press Ctrl+C to stop the server.\n")
            sys.stdout.flush()

            try:
                webbrowser.open(url)
            except Exception:
                pass

            httpd.serve_forever()
            break
        except OSError as e:
            if attempt_port == port + 9:
                print(f"Error: Could not bind to any port between {port} and {attempt_port}: {e}")
                sys.exit(1)
            continue


if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
