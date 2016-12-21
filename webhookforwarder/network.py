import urllib.request


def post_json(payload: str, target: str) -> None:
    payload_ = payload.encode('UTF-8')
    request = urllib.request.Request(target)
    request.add_header('Content-type', 'application/json')
    urllib.request.urlopen(request, payload_)
