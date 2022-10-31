"""Multithreading TSP - server, that receives URL from client, processes them
    and returns 'com_count' most common use words in html"""
import socket
import threading
import queue
import requests
import re
import json
import sys
import argparse
from collections import Counter


class Server:
    def __init__(self, w_count, com_count, host=socket.gethostname(), port=5000):
        print(f'Server ip:{host}, port:{port}')
        self.w_count = w_count
        self.com_count = com_count
        self.url_count = 0
        self.que = queue.Queue(self.w_count * 2)
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.bind((host, port))
        self.ser.listen(self.w_count + 1)

    def sender(self, json_str, url):
        client, addr = self.ser.accept()
        msg = url + '~' + json_str
        client.send('Worker'.encode('utf-8'))
        if client.recv(1024).decode('utf-8') == "Ready":
            client.send(msg.encode('utf-8'))
            self.url_count += 1
        client.close()

    def start_server(self):
        client, addr = self.ser.accept()
        client.send('CLinet is connected!'.encode('utf-8'))

        master_tr = threading.Thread(
                target=self.master,
            )

        master_tr.start()
        master_tr.join()

        print('End')

    def master(self):

        worker_tr = [
            threading.Thread(
                target=self.worker,
            )
            for _ in range(self.w_count)
        ]

        for th in worker_tr:
            th.start()

        while True:
            client, addr = self.ser.accept()
            client.send('Master'.encode('utf-8'))

            try:
                data = client.recv(1024)
            except Exception as e:
                print(f'Error {str(e)}')
                break

            if len(data) > 0:
                url = data.decode('utf-8')[:-1]
                self.que.put(url)
            else:
                for _ in range(self.w_count):
                    self.que.put(None)
                break

            client.close()

        for th in worker_tr:
            th.join()

    def worker(self):
        while True:
            try:
                url = self.que.get(timeout=1)
            except queue.Empty:
                print('Error empty queue')
                continue
            if url is None:
                print('Worker stopped')
                break
            try:
                rs = requests.get(url)
                if rs.status_code != 200:
                    print('Status code is not 200')
                    continue
            except Exception as e:
                print(f'Error: {e}')
                continue

            http = rs.text
            word_list = re.findall('[a-zа-яё]+', http, flags=re.IGNORECASE)
            freq = Counter(word_list).most_common(self.com_count)
            js_freq = json.dumps(dict(freq))
            self.sender(js_freq, url)
            print(js_freq)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=1)
    parser.add_argument('-k', type=int, default=1)
    return parser


if __name__ == '__main__':
    namespace = create_parser().parse_args(sys.argv[1:])
    w = namespace.w
    k = namespace.k
    Server(w, k).start_server()
