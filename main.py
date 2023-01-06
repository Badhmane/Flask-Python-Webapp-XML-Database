from flask import Flask, render_template, request, redirect, url_for, session, g
from xml.dom import minidom
from lxml import etree
from array import *
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, Form, BooleanField, StringField, PasswordField, validators
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, DataRequired
import flask # Import the module
from datetime import datetime

print(flask.__version__)


app = Flask(__name__)
app.secret_key = 'sssseeeeccccrrrreeettttttt'
app.config['UPLOAD_FOLDER'] = 'static/img'

@app.before_request
def befor_request():
    g.user = None
    if 'user_id' in session:
        for user in userObjectCollection:
            if (user.id == session['user_id']):
                g.user = user

########### start xml parser ###########

booksdoc = minidom.parse('xmldata/books.xml')
booksdoc2 = etree.parse('xmldata/books.xml')
usersdoc = minidom.parse('xmldata/users.xml')
ordersdoc = minidom.parse('xmldata/orders.xml')

########### end xml parser ###########
########### start models ###########

# Book


class Book:
    def __init__(self, title, author, publisher, date, types, description, ISBN, price, cover):
        self.types = []
        self.title = title
        self.author = author
        self.publisher = publisher
        self.date = date
        for i in types:
            self.types.append(i)
        self.description = description
        self.ISBN = ISBN
        self.price = price
        self.cover = cover

# User


class Address:
    def __init__(self, house, country, state, zip):
        self.house = house
        self.country = country
        self.state = state
        self.zip = zip


class Cardinfo:
    def __init__(self, name, number, exp, cvv):
        self.name = name
        self.number = number
        self.exp = exp
        self.cvv = cvv


class User:
    def __init__(self, id, fname, lname, email, phone, password, address, cardinfo):
        class Address:
            def __init__(self, house, country, state, zip):
                self.house = house
                self.country = country
                self.state = state
                self.zip = zip

        class Cardinfo:
            def __init__(self, name, number, exp, cvv):
                self.name = name
                self.number = number
                self.exp = exp
                self.cvv = cvv
        self.address = []
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.password = password
        i = 0
        for _ in address:
            self.address.append(
                Address(address[i].house, address[i].country, address[i].state, address[i].zip))
            i = i+1
        i = 0
        self.cardinfo = Cardinfo(
            cardinfo.name, cardinfo.number, cardinfo.exp, cardinfo.cvv)

########### end models ###########
########### start controllers ###########

# Book


books = booksdoc.getElementsByTagName('book')
bookObjectCollection = []
alltypes = []
for book in books:
    types = book.getElementsByTagName('type')
    i = 0
    alltypes.clear()
    for _ in types:
        alltypes.append(types[i].childNodes[0].nodeValue)
        i = i+1
    bookObjectCollection.append(Book(book.getElementsByTagName('title')[0].firstChild.data, book.getElementsByTagName('author')[0].firstChild.data, book.getElementsByTagName('publisher')[0].firstChild.data, book.getElementsByTagName('date')[0].firstChild.data, alltypes,
                                     book.getElementsByTagName('description')[0].firstChild.data, book.attributes['ISBN'].value, book.attributes['price'].value, book.attributes['cover'].value))

# User


users = usersdoc.getElementsByTagName('user')
userObjectCollection = []
addressObjectCollection = []
for user in users:
    # address
    address = user.getElementsByTagName('address')
    houses = user.getElementsByTagName('house')
    countries = user.getElementsByTagName('country')
    states = user.getElementsByTagName('state')
    zips = user.getElementsByTagName('zip')
    i = 0
    try:
        for _ in address:
            addressObjectCollection.append(Address(houses[i].childNodes[0].nodeValue,
                                                   countries[i].childNodes[0].nodeValue,
                                                   states[i].childNodes[0].nodeValue,
                                                   zips[i].childNodes[0].nodeValue))
            i = i+1
    except:
        addressObjectCollection.append(Address("", "", "", ""))

    # cardeinfo
    names = user.getElementsByTagName('name')
    numbers = user.getElementsByTagName('number')
    exps = user.getElementsByTagName('exp')
    cvvws = user.getElementsByTagName('cvv')
    try:
        cardinfoObject = Cardinfo(names[0].childNodes[0].nodeValue,
                                  numbers[0].childNodes[0].nodeValue,
                                  exps[0].childNodes[0].nodeValue,
                                  cvvws[0].childNodes[0].nodeValue)
    except:
        cardinfoObject = Cardinfo("", "", "", "")
    
    userObjectCollection.append(User(user.attributes['id'].value, user.getElementsByTagName('fname')[0].firstChild.data, user.getElementsByTagName('lname')[0].firstChild.data, user.getElementsByTagName('email')[0].firstChild.data, user.getElementsByTagName('phone')[0].firstChild.data, user.getElementsByTagName('password')[0].firstChild.data,
                                     addressObjectCollection, cardinfoObject))

# Addbook


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload")


########### end controllers ###########
########### start views ###########

# Home


@ app.route('/')
@ app.route('/home')
def index():
    booksdoc = minidom.parse('xmldata/books.xml')
    books = booksdoc.getElementsByTagName('book')
    bookObjectCollection.clear()
    for book in books:
        types = book.getElementsByTagName('type')
        i = 0
        alltypes.clear()
        for _ in types:
            alltypes.append(types[i].childNodes[0].nodeValue)
            i = i+1
        bookObjectCollection.append(Book(book.getElementsByTagName('title')[0].firstChild.data, book.getElementsByTagName('author')[0].firstChild.data, book.getElementsByTagName('publisher')[0].firstChild.data, book.getElementsByTagName('date')[0].firstChild.data, alltypes,
                                    book.getElementsByTagName('description')[0].firstChild.data, book.attributes['ISBN'].value, book.attributes['price'].value, book.attributes['cover'].value))
    return render_template('index.html', bookObjectCollection=bookObjectCollection)

# Signup


@ app.route('/signup')
def signup():
    return render_template('signup.html')


# Booklist



@ app.route('/booklist', methods=['POST', 'GET'])
def booklist():

    booksdoc = minidom.parse('xmldata/books.xml')
    books = booksdoc.getElementsByTagName('book')
    bookObjectCollection.clear()
    for book in books:
        types = book.getElementsByTagName('type')
        i = 0
        alltypes.clear()
        for _ in types:
            alltypes.append(types[i].childNodes[0].nodeValue)
            i = i+1
        bookObjectCollection.append(Book(book.getElementsByTagName('title')[0].firstChild.data, book.getElementsByTagName('author')[0].firstChild.data, book.getElementsByTagName('publisher')[0].firstChild.data, book.getElementsByTagName('date')[0].firstChild.data, alltypes,
                                    book.getElementsByTagName('description')[0].firstChild.data, book.attributes['ISBN'].value, book.attributes['price'].value, book.attributes['cover'].value))
    
    if request.method == "POST":
        ISBN = request.form['ISBN']
        if request.form['btn'] == 'Delete':
            books = booksdoc2.getroot()

            for book in books:
                if book.attrib['ISBN'] == ISBN:
                    book.getparent().remove(book)

            bookstr = minidom.parseString(etree.tostring(books, pretty_print=True, encoding='unicode')).toprettyxml()
            bookxml = minidom.parseString(bookstr)
        
            with open("xmldata/books.xml", "w", encoding="utf-8") as xml_file:
                bookxml.writexml(xml_file)
            
            return redirect(url_for('booklist'))
        
    return render_template('booklist.html' , books=bookObjectCollection)


# login


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.pop('user_id', None)
        email = request.form['email']
        password = request.form['password']
        for user in userObjectCollection:
            if (email == user.email and password == user.password):
                session['user_id'] = user.id
                return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('login.html')

# Product



@app.route('/<isbn>', methods=['POST', 'GET'])
def show_product(isbn):
    for book in bookObjectCollection:
        if (isbn == book.ISBN):
            return render_template('product.html', book=book)
    return render_template('404.html')

# Logout


@app.route('/logout')
def logout():
    g.user = None
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Editbook


@ app.route('/<isbn>/editbook', methods=['GET',"POST"])
def editbook(isbn):
    form = UploadFileForm()
    if request.method == "POST":
        ISBN = request.form['isbn']
        price = request.form['price']
        cover = "/static/img/" + request.form['isbn']
        type = request.form['typey']
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        date = request.form['date']
        description = request.form['description']
        # create elements
        Bookk = etree.Element("book", ISBN=ISBN, price=price, cover=cover)
        Title = etree.Element("title")
        Author = etree.Element("author")
        Publisher = etree.Element("publisher")
        Date = etree.Element("date")
        Types = etree.Element("types")
        Description = etree.Element("description")
        # add value
        Title.text = title
        Author.text = author
        Publisher.text = publisher
        Date.text = date
        textt = ''
        for i in type:
            print(textt)
            if i == ',':
                Type = etree.Element("type")
                Type.text = textt
                Types.append(Type)
                textt = ''
            else:
                textt = textt + i
        Type = etree.Element("type")
        Type.text = textt
        Types.append(Type)
        textt = ''
        Description.text = description 
        Types.append(Type)
        Bookk.append(Title)
        Bookk.append(Author)
        Bookk.append(Publisher)
        Bookk.append(Date)
        Bookk.append(Types)
        Bookk.append(Description)
        # Delete the old book
        root = booksdoc2.getroot()
        for book in root:
            if book.attrib['ISBN'] == isbn:
                book.getparent().remove(book)
        
        root.append(Bookk)
        bookstr = minidom.parseString(etree.tostring(root, pretty_print=True, encoding='unicode')).toprettyxml()
        bookxml = minidom.parseString(bookstr)
        
        with open("xmldata/books.xml", "w", encoding="utf-8") as xml_file:
            bookxml.writexml(xml_file)
        
        if form.validate_on_submit():
            file = form.file.data # First grab the file
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(request.form['isbn']  + ".png"))) # Then save the file
    
    for book in bookObjectCollection:
        if (isbn == book.ISBN):
            return render_template('editbook.html', book=book, form=form)
    return render_template('404.html')


# Addbook


@app.route('/addbook', methods=['GET',"POST"])
def addbook():
    form = UploadFileForm()
    if request.method == "POST":
        ISBN = request.form['isbn']
        price = request.form['price']
        cover = "/static/img/" + request.form['isbn']
        type = request.form['typey']
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        date = request.form['date']
        description = request.form['description']
        # create elements
        Bookk = etree.Element("book", ISBN=ISBN, price=price, cover=cover)
        Title = etree.Element("title")
        Author = etree.Element("author")
        Publisher = etree.Element("publisher")
        Date = etree.Element("date")
        Types = etree.Element("types")
        Description = etree.Element("description")
        # add value
        Title.text = title
        Author.text = author
        Publisher.text = publisher
        Date.text = date
        textt = ''
        for i in type:
            print(textt)
            if i == ',':
                Type = etree.Element("type")
                Type.text = textt
                Types.append(Type)
                textt = ''
            else:
                textt = textt + i
        Type = etree.Element("type")
        Type.text = textt
        Types.append(Type)
        textt = ''
        Description.text = description 
        Bookk.append(Title)
        Bookk.append(Author)
        Bookk.append(Publisher)
        Bookk.append(Date)
        Bookk.append(Types)
        Bookk.append(Description)
        root = booksdoc2.getroot()
        root.append(Bookk)
        bookstr = minidom.parseString(etree.tostring(root, pretty_print=True, encoding='unicode')).toprettyxml()
        bookxml = minidom.parseString(bookstr)
        
        with open("xmldata/books.xml", "w", encoding="utf-8") as xml_file:
            bookxml.writexml(xml_file)
        
        if form.validate_on_submit():
            file = form.file.data # First grab the file
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(request.form['isbn']  + ".png"))) # Then save the file
    return render_template('addbook.html', form=form)

########### end views ###########


if __name__ == "__main__":
    app.run(debug=True)
