#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REST app: DB of family

mongod --config ~/github.com/fulkgl/flask1/mongo.conf 

"""

from sys import argv
from pymongo import MongoClient
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, make_response
app = Flask(__name__)

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_406_NOT_ACCEPTABLE = 406


def init_data(use_mongo=False):
    """
    Initialize the data.
    :param use_mongo: bool True to use Mongo (nosql), False use in memory list
    :return: tuple(None, list) for non-Mongo; tuple(mongo_obj, collection_obj)
    """
    mongo_client = None

    if use_mongo:
        #-- connect to mongo server
        mongo_client = MongoClient('mongodb://localhost:27017/')

        #-- DB within mongo
        db_family = mongo_client['family-database']

        #-- get rid of the old table, start new evey time
        db_family['family-collection'].drop()

        #-- collection within DB (nosql collections == sql tables)
        family_data = db_family['family-collection']

    start_with_this_data = [
            { 'name': 'George', 'age': 60, 'city': 'Austin TX', },
            { 'name': 'Meagan', 'age': 29, 'city': 'Norman OK', },
            { 'name': 'Val',    'age': 57, 'city': 'Austin TX', },
            { 'name': 'Sylvia', 'age': 80, 'city': 'Endicott NY', },
    ]
    if use_mongo:
        print("DB is with Mongo")
        if family_data.count() == 0:
            result = family_data.insert_many(start_with_this_data)
    else:
        print("DB is in memory list[]")
        family_data = list(start_with_this_data)

    return mongo_client, family_data


def is_data_valid(data, check_for_name_too=False):
    """
    validate the payload
    must have age:int and city:str
    :param data: dict of data to validate
    :param check_for_name_too: bool True is make sure name field exists
    :return: bool True for good data, False for bad
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
    If name is not None, then return the record or None is not found.
    """
    global family_data, mongo_client
    if name is None:
        # get a list of the names in the DB
        names = []
        if mongo_client is None:
            for record in family_data:
                names.append(record['name'])
        else:
            for record in family_data.find({}, {"_id":0, "name":1}):
                if 'name' in record:
                    names.append(record['name'])
        return names

    if mongo_client is None:
        found = None
        for record in family_data:
            if record['name'] == name:
                found = record
                break
    else:
        found = family_data.find_one({'name':name})
        if found is not None:
            del found['_id']  # get rid of objectid from nosql
    return found


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
    # find the records in our DB (list of found items)
    found = get_list_of_names(name)  # found={rec0}
    if found is None:
        abort(HTTP_404_NOT_FOUND)

    return make_response(jsonify(found), HTTP_200_OK)


@app.route("/members/<string:name>", methods=['POST',])
def create_member(name):
    '''
    POST /member/<name>
    create a new DB record
    We are expecting a json= data record.
    '''
    global family_data, mongo_client
    # does the name already exist?
    names = get_list_of_names()
    if name in names:  # name already in DB
        abort(HTTP_406_NOT_ACCEPTABLE)

    # did we get a json= data?
    if not request.json:  # no payload
        abort(HTTP_400_BAD_REQUEST)

    # validate the data
    new_data = request.json
    if not is_data_valid(new_data):  # payload not valid
        abort(HTTP_400_BAD_REQUEST)
    
    # let's add the name to the record, then add to DB
    new_data['name'] = name
    if mongo_client is None:
        family_data.append(new_data)
    else:
        new_record = dict(new_data)
        # Mongo will change the data type of the object passed to insert_one,
        # so we need to make it a separate object to avoid problems below
        # with the jsonify function.
        family_data.insert_one(new_record)

    # 201 means good create
    return make_response(jsonify({"new_data": new_data}), HTTP_201_CREATED)


@app.route("/members/<string:name>", methods=['PUT',])
def update_member(name):
    '''
    PUT /member/<name>
    update a DB record
    we expect a record update in json=
    '''
    global family_data, mongo_client
    # does the name already exist?
    names = get_list_of_names()
    if name is None:  # name not in DB
        abort(HTTP_404_NOT_FOUND)

    # did we get a json= data?
    if not request.json:  # no payload
        abort(HTTP_400_BAD_REQUEST)

    # validate the data
    data = request.json
    if not is_data_valid(data):  # payload bad
        abort(HTTP_400_BAD_REQUEST)

    found = get_list_of_names(name)
    old_data = dict(found)  # this is the current(old) data

    # update the existing record
    if mongo_client is None:
        found['age'] = data['age']
        found['city'] = data['city']
    else:
        family_data.update_one({'name': name}, {'$set': data})

    return make_response(jsonify({"old_data": old_data}), HTTP_200_OK)


@app.route("/members/<string:name>", methods=['DELETE',])
def delete_member(name):
    '''
    DELETE /member/<name>
    delete a DB record
    '''
    global family_data, mongo_client
    # find the records in our DB (list of found items)
    found = get_list_of_names(name)

    if found is None:
        abort(HTTP_404_NOT_FOUND)

    # copy the record to be removed from the DB (for display in the return)
    deleted_member = dict(found)

    if mongo_client is None:
        family_data.remove(found)
    else:
        family_data.delete_one({'name': name})

    return make_response(jsonify({"deleted_data": deleted_member}), HTTP_200_OK)


if __name__ == "__main__":
    global family_data, mongo_client
    mongo_client, family_data = init_data(
        len(argv) > 1 and argv[1] == "--use-mongo")
    # mongo_client None: means family_data is a list[] of data
    # mongo_client not None: means family_data is mongo collection(aka table)

    app.run(debug=True)

    if mongo_client is not None:
        mongo_client.close()
        mongo_client = None

# END #
