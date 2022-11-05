from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
import hashlib



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()




class Urls(db.Model):
    '''
    sql model (table) which would hold the original url and short url for us
    
    '''
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url(url_received):
    '''
    Function that takes in the url received from the user and generates an short url using md5 hash
    Although the probability of a hash collision is very very less , we still aren't taking any chances
    
    '''
    while True:
        letters = hashlib.md5(url_received.encode('utf-8')).hexdigest()
        letters=str(letters)
        short_url = Urls.query.filter_by(short=letters).first()
        if not short_url:
            return letters


@app.route('/', methods=['POST', 'GET'])
def home():
    '''
    The default endpoint which would take us to the short url generator screen.
    '''
    if request.method == "POST":
        url_received = request.form["nm"]
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url(url_received)
            print(short_url)
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')


@app.route('/<short_url>')
def redirection(short_url):
    '''
    The endpoint which would redirect us to the original url.
    '''

    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'




@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)



@app.route('/all_urls')
def display_all():
    '''
    The endpoint which would show us all the url combinations present in the db.
    '''
    return render_template('all_urls.html', vals=Urls.query.all())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
