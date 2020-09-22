import logging
import subprocess
import urllib
import socket
from subprocess import PIPE
from shlex import quote

from boto3 import session
from snap_api.validator import helper


TEMP_DIR = '/tmp/'
CHROMIUM_CMD = 'chromium-browser --no-sandbox --hide-scrollbars --headless --disable-gpu --screenshot='

def snapshot(url, destination=None):

    try:
        # get site FQDN
        root = urllib.parse.urlparse(url).netloc
        file_path = quote(TEMP_DIR + root + '.png')

        # Security Check for Directory Traversal
        if helper.is_directory_traversal(file_path, TEMP_DIR):
            raise Exception("Bad URL: {}\n".format(url))

        # Check DNS
        pre_cmd = "curl -I {}".format(quote(url))
        pre_proc = subprocess.run(pre_cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        if pre_proc.returncode != 0:
            raise Exception("Not found URL: {}\n".format(url))

        # Take Snapshot
        cmd = "{}{} {}".format(CHROMIUM_CMD, file_path, quote(url))
        proc = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        # print(vars(proc))
        if proc.returncode != 0:
            raise Exception("Process Failed ({}): {}\n".format(proc.returncode, proc.stderr))
        logging.info("Screenshot created: {}\n".format(file_path))
        return file_path

    except Exception as e:
        logging.error(e)
        return None
