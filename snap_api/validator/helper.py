import re
import os

def is_query(query_string):
    if query_string == b'':
        return False

    return True

def has_url_key(query_string):
    if 'url' in query_string.keys():
        return True

    return False

def is_valid_url(url):
    url_reg = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    if re.match(url_reg, url):
        return True
    return False

def is_forbiden_url(url):
    patterns = [
        'localhost',
        '127.0.0.',
        '0.0.0.0'
    ]

    for p in patterns:
        if url.find(p) != -1:
            return True

    return False

def is_directory_traversal(path, limit_path):
    if os.path.commonprefix((os.path.realpath(path), limit_path)) != limit_path:
        return True
    return False