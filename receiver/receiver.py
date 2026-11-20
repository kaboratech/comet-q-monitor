
#!/usr/bin/env python3

# Kaboratech - GL.iNet Comet Q TRMNL Receiver
# Public configuration uses environment variables.
# Do not hardcode private IP addresses or webhook URLs.

import os
import json
import time
import threading
import tempfile
import subprocess
import logging

from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError


BIND_IP = os.environ.get("BIND_IP", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8766"))
ALLOWED_IP = os.environ.get("ALLOWED_SOURCE_IP", "")
WEBHOOK = os.environ.get("TRMNL_WEBHOOK", "")

STATE_FILE = os.environ.get(
    "STATE_FILE",
    "/var/lib/trmnl-cometq/state.json"
)

TIMEOUT = int(os.environ.get("OFFLINE_TIMEOUT", "1200"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

lock = threading.Lock()


def save_state(data):
    directory = os.path.dirname(STATE_FILE)
    os.makedirs(directory, exist_ok=True)

    fd, temporary = tempfile.mkstemp(dir=directory)

    try:
        with os.fdopen(fd, "w") as file:
            json.dump(data, file)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary, STATE_FILE)

    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_state():
    try:
        with open(STATE_FILE) as file:
            return json.load(file)
    except (OSError, ValueError):
        return None


def send_to_trmnl(variables):
    if not WEBHOOK:
        raise RuntimeError("TRMNL_WEBHOOK is not configured")

    payload = json.dumps({"merge_variables": variables})

    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-o",
            "/dev/null",
            "-w",
            "%{http_code}",
            "--max-time",
            "15",
            "-X",
            "POST",
            WEBHOOK,
            "-H",
            "Content-Type: application/json",
            "--data-binary",
            payload
        ],
        capture_output=True,
        text=True,
        timeout=20
    )

    if result.returncode != 0:
        raise URLError(result.stderr.strip() or "curl failed")

    try:
        status = int(result.stdout.strip())
    except ValueError:
        raise URLError("Invalid HTTP response from TRMNL")

    if not 200 <= status < 300:
        raise HTTPError(
            WEBHOOK,
            status,
            "TRMNL rejected the request",
            None,
            None
        )

    return status


def watchdog():
    while True:
        time.sleep(30)

        with lock:
            state = read_state()

            if not state or state.get("offline_sent"):
                continue

            last_seen = state.get("last_seen_epoch", 0)

            if not last_seen or time.time() - last_seen <= TIMEOUT:
                continue

            variables = dict(state.get("variables", {}))

            variables.update({
                "status": "OFFLINE",
                "temperature_c": "OFFLINE",
                "uptime": "OFFLINE",
                "ram_total_mb": "OFFLINE",
                "ram_used_mb": "OFFLINE",
                "ram_available_mb": "OFFLINE",
                "storage_total_mb": "OFFLINE",
                "storage_used_mb": "OFFLINE",
                "storage_free_mb": "OFFLINE",
                "storage_used_percent": "OFFLINE",
                "load_average": "OFFLINE",
                "wifi": "OFFLINE",
                "tailscale": "OFFLINE",
                "local_ip": "OFFLINE"
            })

            try:
                send_to_trmnl(variables)

                state["offline_sent"] = True
                save_state(state)

                logging.warning("Comet Q OFFLINE notification sent")

            except Exception as error:
                logging.error("Failed to send OFFLINE status: %s", error)


class Handler(BaseHTTPRequestHandler):

    def do_POST(self):

        if not ALLOWED_IP:
            self.send_error(403, "Source IP is not configured")
            return

        if self.client_address[0] != ALLOWED_IP:
            self.send_error(403, "Unauthorized source")
            logging.warning(
                "Rejected request from %s",
                self.client_address[0]
            )
            return

        if self.path != "/cometq":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 65536:
                self.send_error(413)
                return

            body = self.rfile.read(length)
            incoming = json.loads(body)

            variables = incoming.get("merge_variables")

            if not isinstance(variables, dict):
                self.send_error(400, "Invalid merge_variables")
                return

            now = time.time()

            variables["status"] = "ONLINE"
            variables["last_seen"] = (
                datetime.now()
                .astimezone()
                .strftime("%Y-%m-%d %H:%M:%S %Z")
            )

            with lock:
                save_state({
                    "last_seen_epoch": now,
                    "offline_sent": False,
                    "variables": variables
                })

                send_to_trmnl(variables)

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

            logging.info("ONLINE data received")

        except (ValueError, KeyError):
            self.send_error(400, "Invalid JSON")

        except (URLError, HTTPError, TimeoutError, OSError) as error:
            logging.error("Communication error: %s", error)
            self.send_error(502, "Failed to forward data to TRMNL")

        except Exception:
            logging.exception("Unexpected error")
            self.send_error(500)

    def do_GET(self):

        if self.path != "/health":
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"receiver":"ready"}')

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":

    if not WEBHOOK:
        raise SystemExit("ERROR: TRMNL_WEBHOOK is not configured")

    if not ALLOWED_IP:
        raise SystemExit("ERROR: ALLOWED_SOURCE_IP is not configured")

    threading.Thread(
        target=watchdog,
        daemon=True
    ).start()

    server = ThreadingHTTPServer((BIND_IP, PORT), Handler)

    logging.info(
        "TRMNL receiver listening on %s:%s",
        BIND_IP,
        PORT
    )

    server.serve_forever()
