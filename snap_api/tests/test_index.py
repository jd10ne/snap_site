import pytest
from snap_api import index
from flask import Flask

@pytest.fixture
def client():
    index.app.config['TESTING'] = True
    with index.app.test_client() as client:
        yield client


def test_take_shot_no_query(client):
    """has no query"""
    res = client.get('/')
    assert b'<title>400 Bad Request</title>' in res.data

def test_take_shot_right_query(client):
    """has right query"""
    res = client.get('/?url=https://www.google.com&url=https://www.yahoo.co.jp')
    assert b'OK' in res.data

def test_take_shot_has_worng_query(client):
    """has wrong query"""
    res = client.get('/?aaa=bbb')
    assert b'<title>400 Bad Request</title>' in res.data

def test_take_shot_has_worng_url(client):
    """has wrong url"""
    res = client.get('/?url=httpsx://www.google.com')
    assert b'<title>400 Bad Request</title>' in res.data

def test_take_shot_has_forbiden_url(client):
    """has wrong url"""
    res = client.get('/?url=http://localhost/')
    assert b'<title>400 Bad Request</title>' in res.data
