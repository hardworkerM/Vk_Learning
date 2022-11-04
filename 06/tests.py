import unittest
from unittest.mock import patch
import socket
import threading
import time
from io import StringIO
from server import Server
from client import Client


class MainTest(unittest.TestCase):
    host = socket.gethostname()

    def run_fake_client(self, port):
        fake_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_client.settimeout(1)
        fake_client.connect((self.host, port))
        msg = fake_client.recv(1024).decode('utf-8')
        fake_client.close()
        return msg

    def stop_fake_client(self, port):
        stop_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stop_socket.connect((self.host, port))
        if stop_socket.recv(1024).decode('utf-8') == 'Master':
            stop_socket.send('Stop'.encode('utf-8'))
        else:
            print('Worker caught')
        stop_socket.close()

    def no_url_fake_client(self, port):
        non_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        non_socket.connect((self.host, port))
        non_socket.close()

    def url_fake_client(self, port, url: str):
        url_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        url_socket.connect((self.host, port))
        url_socket.send(url.encode('utf-8'))
        url_socket.close()
        self.stop_fake_client(port)
        rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rec_socket.connect((self.host, port))
        msg = rec_socket.recv(1024).decode('utf-8')
        rec_socket.send('Ready'.encode('utf-8'))
        url, json_str = rec_socket.recv(1024).decode('utf-8').split('~', 1)
        rec_socket.close()
        return url, json_str, msg

    def run_fake_server(self, port):
        fake_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        fake_server.bind((self.host, port))
        fake_server.listen(1)
        client = fake_server.accept()[0]
        client.send('Exit'.encode('utf-8'))
        client.close()
        fake_server.shutdown(socket.SHUT_RDWR)
        fake_server.close()

    def test_server_connect(self):
        port = 3000
        with patch('builtins.print'):
            server = Server(1, 1, port=port)
            server_thread = threading.Thread(target=server.start_server)
            server_thread.start()
            time.sleep(0.1)
            get_msg = self.run_fake_client(port)
            self.stop_fake_client(port)
            server_thread.join()
            self.assertEqual(get_msg, 'CLinet is connected!')

    def test_server_no_url(self):
        port = 3001
        with patch('sys.stdout', new=StringIO()) as fake_std:
            server = Server(1, 1, port=port)
            server_thread = threading.Thread(target=server.start_server)
            server_thread.start()
            self.run_fake_client(port)
            self.no_url_fake_client(port)
            server_thread.join()
            self.assertEqual(f"Server ip:{self.host},"
                             f" port:{port}\nWorker stopped\nEnd\n",
                             fake_std.getvalue())

    def test_server_master(self):
        port = 3002
        url = 'https://vk.com/\n'
        with patch('builtins.print'):
            server = Server(1, 1, port=port)
            server_thread = threading.Thread(target=server.start_server)
            server_thread.start()
            time.sleep(0.001)
            self.run_fake_client(port)
            res_url, res_json, msg = self.url_fake_client(port, url)[0]
            server_thread.join()
            self.assertEqual(res_url, url[:-1])
            self.assertEqual(msg, 'Worker')

    @patch('builtins.print')
    def test_client_connect(self, mock_print):
        port = 3003
        server_thread = threading.Thread(target=self.run_fake_server,
                                         args=(port,),)
        client = Client(3, 'file.txt', port=port)
        server_thread.start()
        time.sleep(0.001)
        client.connect()
        server_thread.join()
        mock_print.assert_called_with('Wrong connection message from Server')

    @patch('queue.Queue.get')
    def test_worker(self, mock_url):
        mock_url.return_value = None
        ser = Server(1, 1)
        ser.worker()
        ser.close()


if __name__ == '__main__':
    unittest.main()
