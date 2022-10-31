import socket
import threading
import queue
import sys
import argparse


class Client:
    def __init__(self, th_count, file: str, host=socket.gethostname(), port=5000):
        self.file = file
        self.th_count = th_count
        self.host = host
        self.port = port
        self.que = queue.Queue(self.th_count * 2)
        self.lock = threading.Lock()

    def connect(self):
        ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ser.connect((self.host, self.port))
        try:
            msg = ser.recv(1024).decode('utf-8')
        except Exception as e:
            print(f'Error: {str(e)}')
            msg = 'Exit'
            exit()
        if msg == 'CLinet is connected!':
            threads = [
                threading.Thread(
                    target=self.listen,
                )
                for _ in range(self.th_count)
            ]

            for th in threads:
                th.start()

            self.queue_gen()

            for th in threads:
                th.join()
        else:
            exit()

    def queue_gen(self):
        with open(self.file, 'r') as f:
            for line in f:
                self.que.put(line)
        for _ in range(self.th_count):
            self.que.put(None)

    def listen(self):
        while True:
            try:
                ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ser.connect((self.host, self.port))
                msg = ser.recv(1024).decode('utf-8')
            except ConnectionResetError:
                break
            if msg == 'Master':
                url = self.que.get(timeout=1)
                if url is None:
                    break
                ser.send(url.encode('utf-8'))
            elif msg == 'Worker':
                ser.send('Ready'.encode('utf-8'))
                url, json_str = ser.recv(1024).decode('utf-8').split('~', 1)
                print(f'{url}: {json_str}')
            ser.close()


if __name__ == '__main__':
    try:
        num_thr = sys.argv[1]
        file_name = sys.argv[2]
    except IndexError:
        raise IndexError('Not all arguments are given')
    Client(num_thr, file_name).connect()
