from response import Response
import gzip


def decompress(response):
    try:
        if response.headers[b'Content-Encoding'] == b'gzip':
            decompressed_response = Response.from_response(response)
            decompressed_response.content = gzip.decompress(response.content)
            del decompressed_response.headers[b'Content-Encoding']
            return decompressed_response
        else:
            return response
    except KeyError:
        return response


def replace_words(response, words):
    new_response = Response.from_response(response)
    for word in words:
        new_response.content = new_response.content.replace(
            word, b'*' * len(word))
    return new_response
