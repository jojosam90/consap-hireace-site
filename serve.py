"""Run the HireAce site locally.

    python serve.py [port]        (default port: 8000)

Clean URLs work like the live site: /privacy-policy serves privacy-policy.html,
and section URLs (/main, /pricing, ...) or unknown paths serve index.html.
"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        local = os.path.join(ROOT, path.lstrip("/"))
        if not os.path.exists(local) or os.path.isdir(local) and path != "/":
            html = local.rstrip("/") + ".html"
            self.path = "/" + os.path.relpath(html, ROOT).replace(os.sep, "/") if os.path.isfile(html) else "/index.html"
        return super().send_head()

    def end_headers(self):
        # Always fetch fresh files, so edits show up on a normal refresh
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


print(f"HireAce site running at http://localhost:{PORT}  (Ctrl+C to stop)")
http.server.ThreadingHTTPServer(("", PORT), Handler).serve_forever()
