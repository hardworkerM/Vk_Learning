import threading
import requests
import re
import json
import queue
import socket
import sys
from collections import Counter


def master():
    host = socket.gethostname()
    port = 5000
    server = socket.socket()
    server.bind((host, port))
    server.listen(4)
    conn, addr = server.accept()
    print(f'conn={conn}, addr={addr}')
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print(f'from conn user:{data}')

    conn.close()


def worker(url, K):
    print('worker')
    http = requests.get(url).text
    word_list = re.findall('[a-zа-яё]+', http, flags=re.IGNORECASE)
    freq = Counter(word_list).most_common(K)
    js_freq = json.dumps(dict(freq))


if __name__ == '__main__':
    try:
        w_count = sys.argv[1]
        K = sys.argv[2]
    except IndexError:
        raise IndexError('Не все параметры были заданы при запуске')

    que = queue.Queue()
    lock = threading.Lock()

    master_tr = threading.Thread(
            target=master,
        )

    worker_tr = [
        threading.Thread(
            target=worker,
            args=(que, K,),
        )
        for _ in range(w_count)
    ]

    master_tr.start()

    for th in worker_tr:
        th.start()


