#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    #return "Hello flask world"
    #return read_file("index.html")
    return render_template("index.html", name="George")
    
@app.route("/about/<string:myname>")
def about(myname):
    #return "This is George"
    fib = [0,1,2,3,5,8,13,21]
    return render_template("about.html", name=myname,
        fib=fib)
    
@app.route("/member/<string:myname>")
def member(myname):
    return render_template("member.html", title=myname)
    
if __name__ == "__main__":
    app.run(debug=True)
    