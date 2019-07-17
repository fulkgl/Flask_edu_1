#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

host = "http://localhost:5000"

def main():
    global host
    body = {'age': 27, 'city': 'Oklahoma City OK'}
    response = requests.request("POST",
        host+"/members/Laura", json=body)
    print(response.status_code)
    
    resp = requests.request("GET", host+"/members")
    print(resp.status_code)
    print(resp.json())
    
if __name__ == "__main__":
    main()
    