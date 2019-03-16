from flask import Flask, redirect, render_template, g, request
import flask_login

from app import server

# Routes that load templates are listed below:

@server.route("/")
def index():
    return redirect("/login")

@server.route("/login", methods=['GET'])
def login_template():
    return render_template('login.html')

@server.route("/list_item", methods=['GET'])
# @flask_login.login_required
def list_item_template():
    cur = g.db.cursor()
    cur.execute("SELECT * FROM category")
    result=cur.fetchall()
    print result
    cur.close()

    return render_template('list_item.html', categories=result)

@server.route("/list_item", methods=['POST'])
# @flask_login.login_required
def list_item():
    cur = g.db.cursor()
    cur.execute("INSERT INTO item (name, description, condition, categoryname, returnable, startingprice, minimumsaleprice, getitnowprice, endingtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",(
        request.form['item_name'],
        request.form['description'],
        request.form['condition'],
        request.form['category'],
        request.form['returnable'],
        request.form['starting_price'],
        request.form['minimum_price'],
        request.form['get_it_now_price'],
        request.form['ending_time']))

    g.db.commit()
    cur.close()
    return redirect('/list_item')



@server.route("/register", methods=['GET'])
def register_template():
    return render_template('register.html')

@server.route("/register", methods=['POST'])
def register():
    cur = g.db.cursor()
    cur.execute("INSERT INTO regularUser (username, firstname, lastname, password) VALUES (%s, %s, %s, %s);",(
        request.form['user_name'],
        request.form['first_name'],
        request.form['last_name'],
        request.form['user_password']))

    g.db.commit()
    cur.close()
    return redirect('/list_item')

@server.route("/auction")
@flask_login.login_required
def item():
    return render_template('auction.html')

@server.route("/auction/<string:item_ID>/")
# @flask_login.login_required
def getItem(item_ID):
    cur = g.db.cursor()
    # Query the database and obtain data as Python objects
    # cur.execute("SELECT * FROM item WHERE itemid = %s;", item_ID)
    cur.execute("SELECT * FROM item WHERE itemid = %s;" % item_ID)
    result=cur.fetchone()

    if not result:
        #We will do some checking here, but for now just print
        print "No Item"
        cur.close()
        return redirect('/auction')
    else:
        #We will also do some checking here, but for now just print
        print result
        cur.close()
    # return render_template('auction.html', itemID=item_ID, name=name, description=description, condition=condition, categoryname=categoryname, returnable=returnable, startingprice=startingprice, minimumsaleprice=minimumsaleprice, getitnowprice=getitnowprice, endingtime=endingtime)
        return render_template('auction.html', itemID=item_ID, name=result[1], description=result[2], condition=result[3], categoryname=result[4], returnable=result[5], startingprice=result[6], minimumsaleprice=result[7], getitnowprice=result[8], endingtime=result[9])


@server.route("/user-details")
# @flask_login.login_required
def user():
    return render_template('user.html')

@server.route("/user-details/<string:user_name>/")
# @flask_login.login_required
def get_user(user_name):
    cur = g.db.cursor()
    print user_name
    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM regularuser WHERE regularuser.username = '%s';" % user_name)
    result=cur.fetchone()

    if not result:
        #We will do some checking here, but for now just print
        print "No User"
        cur.close()
        return redirect('/user')
    else:
        #We will also do some checking here, but for now just print
        print result
        cur.close()
        return render_template('user.html', username=result[0], firstname=result[1], lastname=result[2])

@server.route("/category")
@flask_login.login_required
def category():
    return render_template('category.html')

@server.route("/category/<string:category_name>/")
@flask_login.login_required
def get_category(category_name):
    cur = g.db.cursor()
    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM item WHERE categoryname = '%s';" % category_name)
    result=cur.fetchall()
    print result

    if not result:
        #We will do some checking here, but for now just print
        print "No Category"
        cur.close()
        return redirect('/category')
    else:
        #We will also do some checking here, but for now just print
        print result
        cur.close()
    # return render_template('auction.html', itemID=item_ID, name=name, description=description, condition=condition, categoryname=categoryname, returnable=returnable, startingprice=startingprice, minimumsaleprice=minimumsaleprice, getitnowprice=getitnowprice, endingtime=endingtime)
        return render_template('category.html', categoryname = category_name, items=result)
