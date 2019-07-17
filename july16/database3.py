#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REST app: DB of family
"""

from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, make_response
app = Flask(__name__)

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_406_NOT_ACCEPTABLE = 406

def init_data():
    return [
            { 'name': 'George', 'age': 60, 'city': 'Austin TX', },
            { 'name': 'Meagan', 'age': 29, 'city': 'Norman OK', },
            { 'name': 'Val',    'age': 57, 'city': 'Austin TX', },
            { 'name': 'Sylvia', 'age': 80, 'city': 'Endicott NY', },
    ]
global DB
DB = init_data()


def is_data_valid(data, check_for_name_too=False):
    """
    validate the payload
    must have age:int and city:str
    """
    if 'age' not in data or \
            'city' not in data or \
            not isinstance(data['age'], int) or \
            not isinstance(data['city'], str):
        return False
    if check_for_name_too:
        if 'name' not in data or \
                not isinstance(data['name'], str):
            return False
    return True


def get_list_of_names(name=None):
    """
    Return a list of names in the DB.
    :param name: str name, if None then return a list of all names
    """
    global DB
    if name is None:
        # ['aaa', 'bbb', ...]
        return [record['name'] for record in DB]

    # [{'name': 'x', 'age': 0, 'city': 'y',},]
    return [record for record in DB if record['name'] == name]


@app.route("/members")
def get_all_members():
    '''
    GET /member
    retrieve a list of all members
    '''
    # get the list of names
    names = get_list_of_names()  # names=['aaa','bbb',...]
    return make_response(jsonify({"names": names}), HTTP_200_OK)


@app.route("/members/<string:name>", methods=['GET',])
def get_a_member(name):
    '''
    GET /member/<name>
    retrieve a data for the specified member
    '''
    global DB
    # find the records in our DB (list of found items)
    found = get_list_of_names(name)  # found=[{rec0},]
    if len(found) == 0:  # name not in DB
        abort(HTTP_404_NOT_FOUND)
    if len(found) > 1:  # multiply names DB. corrupt?
        abort(HTTP_406_NOT_ACCEPTABLE)

    return make_response(jsonify(found[0]), HTTP_200_OK)


@app.route("/members/<string:name>", methods=['POST',])
def create_member(name):
    '''
    POST /member/<name>
    create a new DB record
    We are expecting a json= data record.
    '''
    # does the name already exist?
    names = get_list_of_names()
    if name in names:  # name already in DB
        abort(HTTP_406_NOT_ACCEPTABLE)

    # did we get a json= data?
    if not request.json:  # no payload
        abort(HTTP_400_BAD_REQUEST)

    # validate the data
    data = request.json
    if not is_data_valid(data):  # payload not valid
        abort(HTTP_400_BAD_REQUEST)
    
    # let's add the name to the record, then add to DB
    data['name'] = name
    DB.append(data)

    # 201 means good create
    return make_response(jsonify({"new_data": data}), HTTP_201_CREATED)


@app.route("/members/<string:name>", methods=['PUT',])
def update_member(name):
    '''
    PUT /member/<name>
    update a DB record
    we expect a record update in json=
    '''
    # does the name already exist?
    names = get_list_of_names()
    if name not in names:  # name not in DB
        abort(HTTP_404_NOT_FOUND)

    # did we get a json= data?
    if not request.json:  # no payload
        abort(HTTP_400_BAD_REQUEST)

    # validate the data
    data = request.json
    if not is_data_valid(data):  # payload bad
        abort(HTTP_400_BAD_REQUEST)

    found = get_list_of_names(name)
    old_data = dict(found[0])  # this is the current(old) data

    # update the existing record
    found[0]['age'] = data['age']
    found[0]['city'] = data['city']

    return make_response(jsonify({"old_data": old_data}), HTTP_200_OK)


@app.route("/members/<string:name>", methods=['DELETE',])
def delete_member(name):
    '''
    DELETE /member/<name>
    delete a DB record
    '''
    global DB
    # find the records in our DB (list of found items)
    found = get_list_of_names(name)

    if len(found) == 0: # name not found
        abort(HTTP_404_NOT_FOUND)
    if len(found) > 1: # multi names
        abort(HTTP_406_NOT_ACCEPTABLE)

    # remove the one record from the DB
    delete_member = dict(found[0])
    DB.remove(found[0])

    return make_response(jsonify({"deleted_data": delete_member}), HTTP_200_OK)


if __name__ == "__main__":
    app.run(debug=True)

# END #
