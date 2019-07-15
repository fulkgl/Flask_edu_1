#!/usr/bin/python

from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from toy import Toy

app = Flask(__name__)
modus = Modus(app)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')
toys = [duplo,lego,knex]

@app.route('/toys/new')
def new():
    return render_template('new.html')

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # gather the value of an input with a name attribute of "name"
        toys.append(Toy(request.form['name']))
        # respond with a redirect to the route which has a function called "index" (in this case that is '/toys')
        return redirect(url_for('index'))
    # if the method is GET, just return index.html
    return render_template('index.html', toys=toys)

'''
@app.route('/toys/<int:id>')
def show(id):
    # find a toy based on its id
    for toy in toys:
        if toy.id == id:
            found_toy = toy
    # Refactor the code above using a list comprehension!

    return render_template('show.html', toy=found_toy)
'''

@app.route('/toys/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    # Refactored using a generator so that we do not need to do [0]!
    found_toy = next(toy for toy in  toys if toy.id == id)

    # if we are updating a toy...
    if request.method == b"PATCH":
        found_toy.name = request.form['name']
        return redirect(url_for('index'))

    if request.method == b"DELETE":
        toys.remove(found_toy)
        return redirect(url_for('index'))
    # if we are showing information about a toy
    return render_template('show.html', toy=found_toy)

@app.route('/toys/<int:id>/edit')
def edit(id):
    # Refactored using a list comprehension!
    found_toy = [toy for toy in  toys if toy.id == id][0]
    # Refactor the code above to use a generator so that we do not need to do [0]!
    return render_template('edit.html', toy=found_toy)


