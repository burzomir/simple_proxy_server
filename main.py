import threading
import time
from proxy_server import ProxyServer
from response_processors import decompress, replace_words

words_to_censore = [
    'stacji',
    'ROZKŁAD JAZDY'
]


class ReplacingProxyServer(ProxyServer):
    def process_response(self, response):
        if b'text/html' in response.headers.get(b'Content-Type', b''):
            response = replace_words(decompress(response), [bytes(word.encode('utf-8')) for word in words_to_censore])
        
        print(response.get_raw_response())
        return response


server = ReplacingProxyServer()

try:
    server.start()
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    server.stop()

    


