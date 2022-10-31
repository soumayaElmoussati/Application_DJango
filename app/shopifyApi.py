import wra
from shopify import session_token

class shopifyApi():

    apiSecret = None
    apiKey = None
    def __init__(self, apiKey, apiSecret):
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    decoded_payload = session_token.decode_from_header(
    authorization_header=your_auth_request_header,
    api_key=apiKey,
    secret=apiSecret,
    )