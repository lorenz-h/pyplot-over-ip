import matplotlib.pyplot as plt
import pickle
import requests
from typing import Optional
import sys
from matplotlib.figure import Figure


RECEIVER_HOST = None
RECEIVER_PORT = None
RECEIVER_PASSWORD = None


def setup(host: str, password: str, port: int = 8137):
    global RECEIVER_HOST
    global RECEIVER_PASSWORD
    global RECEIVER_PORT

    RECEIVER_HOST = host
    RECEIVER_PASSWORD = password
    RECEIVER_PORT = port


def show(fig: Optional[Figure] = None):
    if fig is None:
        fig = plt.gcf()
    if RECEIVER_HOST is None or RECEIVER_PORT is None or RECEIVER_PASSWORD is None:
        raise RuntimeError("You must specify the receiver using pyplot_over_ip.setup() before calling show.")
    resp = requests.post(f"http://{RECEIVER_HOST}:{RECEIVER_PORT}/",
                         data=pickle.dumps(fig), auth=("pltoip", RECEIVER_PASSWORD))
    
    if resp.status_code >= 400:
        print(resp)


def handshake(host: str, port: int, password: str):
    sys_version = "Python/" + sys.version.split()[0]
