from flask import abort
from urllib import parse
import logging
import os
from . import helper

ACCEPT_HEADER = os.environ['ACCEPT_HEADER'] if 'ACCEPT_HEADER' in os.environ.keys() else 'Aniapp'
ACCEPT_STR = os.environ['ACCEPT_STR'] if 'ACCEPT_STR' in os.environ.keys() else 'test'

def take_snap(request):

    # request has no query
    hit = helper.is_query(request.query_string)

    # parse query strings
    q = parse.parse_qs(request.query_string.decode('utf-8'))
    hit = hit and helper.has_url_key(q)

    # has no url param => error
    if not hit:
        logging.error('URL Parameters are invalid: {}'.format(q))
        return abort(400)

    # check url
    urls = q['url']
    for u in urls:
        hit = hit and helper.is_valid_url(u)
        hit = hit and not helper.is_forbiden_url(u)

    if not hit:
        logging.error('URLs are invalid: {}'.format(q))
        return abort(400)

def check_header(headers):
    if headers.get(ACCEPT_HEADER) != ACCEPT_STR:
        logging.warning('Unauthorized Access: {}'.format(headers))
        return abort(403)
