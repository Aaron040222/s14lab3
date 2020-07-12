from flask import Flask, render_template, request, redirect, url_for
from models.users import Db, User
from modules.userform import UserForm
from modules.deleteform import DeleteForm
from modules.updateform import UpdateForm
from modules.randomform import RandomForm
import psycopg2
import random
import string
from modules.specificform import SpecificForm
from flask_heroku import Heroku
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgresql-cubed-05568')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Db.init_app(app)


@app.route('/')
def index():
    # Query all
    users = User.query.all()

    for user in users:
       	User.toString(user)

    return render_template("index.html",user=user,users=users)

@app.route('/specificuser', methods=['GET', 'POST'])
def specificUser():
    form = SpecificForm()
    # If GET
    if request.method == 'GET':
        return render_template('specificuser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            specificuser = User.query.filter_by(first_name=first_name).first()
            return render_template('showuser.html',specificuser=specificuser)
        else:
            return render_template('specificuser.html', form=form)

# @route /adduser/<first_name>/<age>
@app.route('/specificuser/<first_name>')
def specificUserFromUrl(first_name):
    specificuser = User.query.filter_by(first_name=first_name).first()
    return render_template('showuser.html',specificuser=specificuser)


# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)

# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    Db.session.add(User(first_name=first_name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))


@app.route('/deleteuser', methods=['GET', 'POST'])
def DeleteUser():
    form = DeleteForm()
    # If GET
    if request.method == 'GET':
        return render_template('deleteuser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            user_id = request.form['user_id']
            delete_user = User.query.filter_by(user_id=user_id).first()
            Db.session.delete(delete_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('deleteuser.html', form=form)

# @route /adduser/<first_name>/<age>
@app.route('/deleteuser/<user_id>')
def deleteUserFromUrl(user_id):
    Db.session.delete(User(user_id=user_id))
    Db.session.commit()
    return redirect(url_for('index'))

@app.route('/updateuser', methods=['GET', 'POST'])
def UpdateUser():
    form = UpdateForm()
    # If GET
    if request.method == 'GET':
        return render_template('updateuser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            user_id = request.form['user_id']
            udfirst_name = request.form['first_name']
            udage = request.form['age']
            update_user = User.query.filter_by(user_id=user_id).first()
            update_user.first_name = udfirst_name
            update_user.age = udage
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('updateuser.html', form=form)

@app.route('/updateuser/<user_id>/<udfirst_name>/<udage>')
def updateUserFromUrl(user_id,udfirst_name,udage):
    update_user = User.query.filter_by(user_id=user_id).first()
    update_user.first_name = udfirst_name
    update_user.age = udage
    Db.session.commit()
    return redirect(url_for('index'))

@app.route('/randomuser', methods=['GET', 'POST'])
def RandomUser():
    form = RandomForm()
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    # If GET
    if request.method == 'GET':
        return render_template('randomuser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            randomnumber = int(request.form['numberofusers'])
            for i in range (randomnumber):
            	result_str = ''.join(random.choice(letters) for x in range(5))
            	first_name = result_str
            	age = random.randrange(100)
            	new_user = User(first_name=first_name, age=age)
            	Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('randomuser.html', form=form)

@app.route('/randomuser/<numberofusers>')
def randomUserFromUrl(numberofusers):
    randomnumber = int(request.form['numberofusers'])
    for i in range (randomnumber):
        result_str = ''.join(random.choice(letters) for x in range(5))
        first_name = result_str
        age = random.randrange(100)
        new_user = User(first_name=first_name, age=age)
        Db.session.add(new_user)
    Db.session.commit()
    return redirect(url_for('index'))

