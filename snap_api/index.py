from flask import Flask, request, abort, Response, jsonify
from urllib import parse
import logging
import os
from snap_api.validator import valid as v
from snap_api.browser_driver import snap
import snap_api.tranfer as tf

app = Flask(__name__)
# Enable UTF-8
app.config["JSON_AS_ASCII"] = False
logging.basicConfig(level=logging.DEBUG)

BUCKET=os.environ['BUCKET']

@app.route('/', methods=['GET'])
def take_snap():
    v.check_header(request.headers)

    v.take_snap(request)
    urls = parse.parse_qs(parse.unquote(request.query_string.decode('utf-8')))['url']

    thumnails = {}
    for u in urls:
        file_path = snap.snapshot(u, None)
        if file_path is None: abort(500)
        presigned_url = tf.put_obj(file_path, BUCKET)
        if presigned_url is None: abort(500)

        thumnails[u] = presigned_url
    print(thumnails)
    return jsonify(thumnails), 200