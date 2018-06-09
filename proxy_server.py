import socket
import threading
from urllib.parse import urlparse
import time
import gzip
from response import Response


class ProxyServer:

    def __init__(self):
        self.is_running = False

    def start(self):
        self.is_running = True
        thread = threading.Thread(target=self.listen)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.is_running = False

    def process_response(self, response):
        return response

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 9000))
            s.listen(1)
            s.settimeout(1)
            while self.is_running:
                try:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handle_client, args=(conn,)).start()
                except socket.timeout:
                    pass

    def handle_client(self, conn):
        try:
            with conn:
                conn.settimeout(1)
                request_data = conn.recv(1024)
                hostname = ProxyServer.get_hostname(request_data)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((hostname, 80))
                    s.sendall(request_data)
                    raw_response = self.recv_timeout(s)
                    response = Response.from_raw_response(raw_response)
                    conn.sendall(self.process_response(response).get_raw_response())

        except socket.timeout:
            pass

    def recv_timeout(self, socket, timeout=2):
        socket.setblocking(0)
        total_data = []
        data = ''
        begin = time.time()
        while 1:
            if total_data and time.time()-begin > timeout:
                break
            elif time.time()-begin > timeout*2:
                break
            try:
                data = socket.recv(8192)
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        return b''.join(total_data)

    @staticmethod
    def get_hostname(request_data):
        url = urlparse(request_data.split(b' ')[1])
        hostname = url.hostname
        return hostname
