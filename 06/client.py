import socket
import threading
import queue
import sys


def threaded(que, client):
    while True:
        url = que.get(timeout=1)
        if url is None:
            break
        client.send(url)


def connect(m, f):
    que = queue.Queue(m*2)
    host = socket.gethostname()
    port = 5000
    client = socket.socket()
    client.connect((host, port))

    with open(f, 'rb') as f:

        threads = [
            threading.Thread(
                target=threaded,
                args=(que, client,),
            )
            for _ in range(m)
        ]
        for th in threads:
            th.start()

        for line in f:
            que.put(line)

        for _ in range(m):
            que.put(None)

    client.close()


if __name__ == '__main__':
    try:
        M = sys.argv[1]
        file = sys.argv[2]
    except IndexError:
        raise IndexError('Не все параметры были заданы при запуске')
    connect(M, file)
