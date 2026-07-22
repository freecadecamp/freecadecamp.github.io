"""
Robust HTTP server with Range request support for video streaming.
Handles partial content requests so browsers can seek/stream videos.
"""
import http.server
import os
import sys

class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        f = None

        if os.path.isdir(path):
            return super().send_head()

        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        fs = os.fstat(f.fileno())
        file_size = fs.st_size

        # Handle Range requests for video streaming
        range_header = self.headers.get('Range')
        if range_header:
            try:
                range_val = range_header.strip().split('=')[1]
                start_str, end_str = range_val.split('-')
                start = int(start_str) if start_str else 0
                end = int(end_str) if end_str else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1

                f.seek(start)
                self.send_response(206)
                ctype = self.guess_type(path)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f
            except Exception:
                pass

        # Normal full-file response
        self.send_response(200)
        ctype = self.guess_type(path)
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", str(file_size))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, BrokenPipeError):
            pass  # Client disconnected — not a crash

    def log_message(self, format, *args):
        # Suppress noisy logs, only show errors
        if args and len(args) >= 2 and str(args[1]) not in ('200', '206', '304', '404'):
            super().log_message(format, *args)
        elif args and len(args) >= 2 and str(args[1]) == '404':
            super().log_message(format, *args)


PORT = 8080
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with http.server.ThreadingHTTPServer(("", PORT), RangeHTTPRequestHandler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    sys.stdout.flush()
    httpd.serve_forever()
