from urllib import request
from flask import Flask, render_template, url_for, flash, redirect,request
from flask_behind_proxy import FlaskBehindProxy
from main_ebay import Ebay_21
from zappos import Zappos
import requests
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

key = secrets.token_hex(16)
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Liked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.description}', '{self.url}')"

class SaveLiked(FlaskForm):
    submit = SubmitField('Liked')

with app.app_context():
    # db.drop_all()
    db.create_all()

@app.route("/",methods=['GET', 'POST'])
@app.route("/index",methods=['GET', 'POST'])
def index():
    form = SaveLiked()
    print('hi')
    if form.validate_on_submit():
        print('works')
        saved_liked(24, "hat", "cat") # do something
        print('data')
        print(db.session.query(Liked).all())
    if request.method == 'POST':
        search_query = request.form.get('search')
        flash(f"Search Query: {search_query}")
        ebay = Ebay_21(name=search_query)
        zappos_data = Zappos(search_query)
        # Use the ebay object as needed
        #flash(f"Search Query: {search_query}")
        return f"<h1> Ebay </h1> <table>{ebay.retrieve_data_from_database()}</table> <h1> ZAPPOS </h1> <table>{zappos_data.returnDatabase()}</table> "
        #return redirect(url_for('liked'))  # Redirect back to the index page after form submission
    return render_template('base.html', form=form)
    
@app.route("/liked")
def liked():
    return render_template('liked.html')

@app.route("/products")
def products():
    return render_template('products.html')

def saved_liked(id, description, url):
    liked = Liked(id=id, description=description, url=url) 
    db.session.add(liked)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = 8001)