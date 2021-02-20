import http.server
import json
from typing import Tuple, List
import argparse

import pickle
from matplotlib.figure import Figure
from base64 import b64decode, b64encode
import multiprocessing as mp
import matplotlib.pyplot as plt
from queue import Empty as EmptyQueueException


def _window_handler(queue: mp.Queue):
    plt.ion()
    plt.show()
    while True:
        try:
            fig = queue.get(block=False)
            plt.figure(fig.number)
        except EmptyQueueException:
            pass
        finally:
            plt.pause(0.001)



class PlotRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        auth_header = self.headers.get("Authorization", "no auth provided")
        
        if auth_header[6:] != self.server.basic_auth:
            print(f"Authentication error: Authorization header was: {auth_header}")
            self.send_response(401)
            self.end_headers()
            return

        post_data = self.rfile.read(content_length)

        fig: Figure = pickle.loads(post_data)
        assert isinstance(fig, Figure), f"Received invalid python object {fig}. Can only send matplotlib.figure.Figure"    
        print(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")

        success = self.server.show_figure(fig)
        if success:
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(500)
            self.end_headers()
        

    def do_GET(self):
        print('server', self.server)
        print(f"Got get request for {self.path}")
        if self.path == "/status":

            print("AUTH", self.headers.get("Authorization"))

            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ready", "sys_version": self.server.sys_version}).encode("utf-8"))
        else:
            self.send_response(404)


class PlotReceiver(http.server.HTTPServer):
    def __init__(self, host: str, port: int, password) -> None:
        self.basic_auth = b64encode(f"pltoip:{password}".encode("utf-8")).decode("ascii")
        self.figure_queue = mp.Queue()
        self.window_handler = mp.Process(target=_window_handler, args=[self.figure_queue], daemon=True)
        self.window_handler.start()
        super().__init__((host, port), PlotRequestHandler)

    def show_figure(self, fig: Figure) -> bool:
        self.figure_queue.put(fig)
        return self.window_handler.is_alive()

    def serve_forever(self) -> None:
        print(f"Receiver listening at {self.server_address}")
        return super().serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Receiver for pyplot-over-ip")

    parser.add_argument("--address", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8137)
    parser.add_argument("--password", type=str, required=True)
    args = parser.parse_args()

    s = PlotReceiver(args.address, args.port, args.password)
    s.serve_forever()
