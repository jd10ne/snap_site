from flask import Flask, request, abort, Response
from urllib import parse
import logging
from snap_api.validator import valid as v
from snap_api.browser_driver import snap

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def take_snap():
    v.take_snap(request)
    urls = parse.parse_qs(request.query_string.decode('utf-8'))['url']
    for u in urls:
        file_path = snap.snapshot(u, None)
        if file_path is None: abort(500)
        logging.info(file_path)
    return Response('OK')