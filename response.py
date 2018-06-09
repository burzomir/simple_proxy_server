class Response:

  @staticmethod
  def from_raw_response(raw_response):
    response_data = raw_response.split(b'\r\n')
    response = Response()
    response.preamble = response_data[0]
    headers_end_index = 0


    for index, raw_header in enumerate(response_data[1:]):
      if raw_header == b'': 
        headers_end_index = index
        break
      chunks = raw_header.split(b': ')
      key = chunks[0]
      value = chunks[1]
      response.headers[key] = value

    response.content = b'\r\n'.join(response_data[headers_end_index + 2:])

    return response

  @staticmethod
  def from_response(response):
    new_response = Response()
    new_response.preamble = response.preamble
    new_response.headers = response.headers.copy()
    new_response.content = response.content
    return new_response

  def __init__(self):
    self.preamble = None
    self.headers = {}
    self.content = None

  def get_raw_response(self):
    return self.preamble + b'\r\n' + self.get_raw_headers() + b'\r\n\r\n' + self.content

  def get_raw_headers(self):
    return b'\r\n'.join([self.get_raw_header(key) for key in self.headers.keys()])

  def get_raw_header(self, key):
    value = self.headers[key]
    return key + b': ' + value
    

