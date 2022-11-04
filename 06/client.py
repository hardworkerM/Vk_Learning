"""Client code that parse file with urls, sends
urls one by one to server and receives the result"""
import socket
import threading
import queue
import sys


class Client:
    """Client takes such values as th_count - number of threads,
    file - name of file which client will send to server,
    host and port"""
    def __init__(self, th_count, file: str,
                 host=socket.gethostname(), port=5000):
        self.file = file
        self.th_count = th_count
        self.host = host
        self.port = port
        self.que = queue.Queue(self.th_count * 2)

    def connect(self):
        """Check connection to server, starts threads,
        fills a queue with urls from the file,
        exits if there is no connection"""
        ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ser.connect((self.host, self.port))
        try:
            msg = ser.recv(1024).decode('utf-8')
        except ConnectionResetError:
            print('ConnectionResetError')
            msg = 'Exit'
        if msg == 'CLinet is connected!':
            print(msg)
            threads = [
                threading.Thread(
                    target=self.listen,
                )
                for _ in range(self.th_count)
            ]

            for thread in threads:
                thread.start()

            self.queue_gen()

            for thread in threads:
                thread.join()
        else:
            print("Wrong connection message from Server")
        ser.close()

    def queue_gen(self):
        """Fills queue with urls from given file"""
        with open(self.file, 'r', encoding='utf-8') as text:
            for line in text:
                self.que.put(line)
        for _ in range(self.th_count):
            self.que.put(None)

    def listen(self):
        """Threads that in loop connect to the server
        if server sends 'Master' they send it an url from queue,
        if server sends 'Worker' they are waiting to receive
        result from server and print it"""
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
        M = int(sys.argv[1])
        file_name = sys.argv[2]
    except IndexError as exc:
        raise exc
    Client(M, file_name).connect()
