#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test the database rest apis

python -m pytest test_database.py
python -m pytest test_database.py::test_post_good

"""

import pytest
import json
import requests

host = "http://localhost:5000"

def test_get1():
    # curl -i http://localhost:5000/members
    global host
    response = requests.request("GET", host+"/members")
    assert response.status_code == 200
    assert response.reason == "OK"
    data = response.json()
    assert data == {'names': ['George', 'Meagan', 'Val', 'Sylvia',]}

def test_get2_good():
    # curl -i http://localhost:5000/members/George
    global host
    response = requests.request("GET", host+"/members/George")
    assert response.status_code == 200
    assert response.reason == "OK"
    data = response.json()
    assert data == {'age': 60, 'city': 'Austin TX', 'name': 'George'}

def test_get2_bad_name():
    # curl -i http://localhost:5000/members/badName
    global host
    response = requests.request("GET", host+"/members/badName")
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"
    assert response.ok is False
    # no response.json()

@pytest.mark.skip(reason="need to setup invalid multi-name DB")
def test_get2_multi_names():
    global host
    response = requests.request("GET", host+"/members/multiNames")
    assert response.status_code == 406

def test_post_dup_name():
    # George already exists so it should fail
    global host
    response = requests.request("POST", host+"/members/George")
    assert response.status_code == 406
    assert response.ok is False
    assert response.reason == "NOT ACCEPTABLE"

def test_post_good():
    # curl -i -H "Content-Type: application/json" -X POST -d '{"age":27,"city":"Oklahoma City OK"}' http://localhost:5000/members/Laura
    global host
    body = {'age': 27, 'city': 'Oklahoma City OK'}
    response = requests.request("POST", host+"/members/Laura", json=body)
    assert response.status_code == 201
    assert response.json() == {'new_data': {'name': 'Laura', 'age': 27, 'city': 'Oklahoma City OK',}}

    # after adding Laura to the DB, let's see that she's really there
    response2 = requests.request("GET", host+"/members")
    assert response2.status_code == 200
    print( response2.json() )
    assert response2.json() == {'names': [
        'George', 'Meagan', 'Val', 'Sylvia', 'Laura', ]}

def test_put():
    #curl -i -H "Content-Type: application/json" -X PUT -d '{"age":27,"city":"Mustang OK"}' http://localhost:5000/members/Laura
    global host
    body = {'age': 27, 'city': 'Mustang OK'}
    response = requests.request("PUT", host+"/members/Laura", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data == {'old_data': {'name': 'Laura', 'age': 27, 'city': 'Oklahoma City OK'}}

def test_delete_badname():
    global host
    response = requests.request("DELETE", host+"/members/badName")
    assert response.status_code == 404

def test_delete_good():
    #curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/members/Laura
    global host
    response = requests.request("DELETE", host+"/members/Laura")
    assert response.status_code == 200
    assert response.json() == {'deleted_data':
            {'name': 'Laura', 'age': 27, 'city': 'Mustang OK'}}


