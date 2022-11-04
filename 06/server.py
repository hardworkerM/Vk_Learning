"""Multithreading TSP - server, that receives URL from client, processes
    them and returns N most common use words in html"""
import socket
import threading
import queue
import re
import json
import sys
import argparse
from collections import Counter
import requests


class Server:
    """Server takes such values as w_count - number of worker threads,
    com_count - number of most common use words in html
    host and port"""
    def __init__(self, w_count=1, com_count=1,
                 host=socket.gethostname(), port=5000):
        print(f'Server ip:{host}, port:{port}')
        self.w_count = w_count
        self.com_count = com_count
        self.lock = threading.Lock()
        self.url_count = 0
        self.que = queue.Queue(self.w_count * 2)
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ser.bind((host, port))
        self.ser.listen(self.w_count + 1)

    def sender(self, json_str, url):
        """Connects to client and sends processed url
         when Client sends 'Ready', count a number of processed urls"""
        client = self.ser.accept()[0]
        msg = url + '~' + json_str
        client.send('Worker'.encode('utf-8'))
        if client.recv(1024).decode('utf-8') == "Ready":
            client.send(msg.encode('utf-8'))
            self.url_count += 1
        client.close()

    def start_server(self):
        """Checks connection to the client and
        starts up the master thread"""
        client = self.ser.accept()[0]
        client.send('CLinet is connected!'.encode('utf-8'))
        client.close()

        master_tr = threading.Thread(
                target=self.master,
            )

        master_tr.start()
        master_tr.join()

        self.ser.close()
        print('End')

    def master(self):
        """Starts up worker threads, in loop connects to the
        client, receives url from client and puts it in queue"""
        worker_tr = [
            threading.Thread(
                target=self.worker,
            )
            for _ in range(self.w_count)
        ]

        for thread in worker_tr:
            thread.start()

        while True:
            client = self.ser.accept()[0]
            client.send('Master'.encode('utf-8'))

            try:
                data = client.recv(1024)
            except ConnectionResetError:
                print('ConnectionResetError')
                break

            if data.decode('utf-8') == 'Stop':
                print('Server stopped')
                for _ in range(self.w_count):
                    self.que.put(None)
                break
            if len(data) > 0:
                url = data.decode('utf-8')[:-1]
                self.que.put(url)
            else:
                for _ in range(self.w_count):
                    self.que.put(None)
                break

            client.close()
        client.close()

        for thread in worker_tr:
            thread.join()

    def worker(self):
        """Worker threads in loop take urls from the queue,
        take html from url and count most common words and
        send the result to client"""
        while True:
            try:
                url = self.que.get(timeout=1)
            except queue.Empty:
                print('Waiting for url...')
                continue
            if url is None:
                print('Worker stopped')
                break
            try:
                request = requests.get(url, timeout=10)
                if request.status_code != 200:
                    print('Status code is not 200')
                    continue
            except requests.exceptions.RequestException as ex:
                print(f'Exception: {str(ex)}')
                continue

            http = request.text
            word_list = re.findall('[a-zа-яё]+', http, flags=re.IGNORECASE)
            freq = Counter(word_list).most_common(self.com_count)
            js_freq = json.dumps(dict(freq))
            self.sender(js_freq, url)
            with self.lock:
                print(f'Number of processed urls is: {self.url_count}')

    def close(self):
        """Closes the server"""
        self.ser.shutdown(socket.SHUT_RDWR)
        self.ser.close()


def create_parser():
    """Parsed arguments that given in the start of .py script"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=1)
    parser.add_argument('-k', type=int, default=1)
    return parser


if __name__ == '__main__':
    namespace = create_parser().parse_args(sys.argv[1:])
    w = namespace.w
    k = namespace.k
    Server(w, k).start_server()
