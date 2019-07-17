#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

host = "http://localhost:5000"

def add(new_name, payload):
    global host
    resp = requests.request("POST", host+"/members/"+new_name,
        json=payload)
    print(resp.status_code)
    print(resp.json())

def main():
    global host
    resp = requests.request("GET", host+"/members")
    print(resp)
    print(resp.status_code)
    print(resp.json())
    return
    
if __name__ == "__main__":
    add("Laura", {'age': 27, 'city': "OKC"})
    