from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3
from flask_bcrypt import Bcrypt


app=Flask(__name__)
app.config['SECRET_KEY'] = 'thisIsSecret'
login_manager = LoginManager(app)
login_manager.login_view="login"



class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password
        self.authenticated = False
    def is_active(self):
            return self.is_active()
    def is_anonymous(self):
            return False
    def is_authenticated(self):
            return self.authenticated
    def is_active(self):
            return True
    def get_id(self):
            return self.id


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    con = sqlite3.connect("login.db")
    curs = con.cursor()
    email= request.form['email']
    curs.execute("SELECT * FROM login where email = (?)", [email])
    row = curs.fetchone()
    if row==None:
        flash('Please try logging in again')
        return render_template('login.html')
    user =list(row);
    liUser = User(int(user[0]),user[1],user[2])
    password = request.form['password']
    match = liUser.password==password
    if match and email==liUser.email:
        login_user(liUser,remember=request.form.get('remember'))
        redirect(url_for('home'))
    else:
        flash('Please try logging in again')
        return render_template('login.html')
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('login.db')
    curs = conn.cursor()
    curs.execute("SELECT * from login where user_id = (?)", [user_id])
    liUser = curs.fetchone()
    if liUser is None:
        return None
    else:
        return User(int(liUser[0]), liUser[1], liUser[2])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/enternew')
@login_required
def new_student():
    return render_template('student.html')

@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['addr']
            city = request.form['city']

            with sqlite3.connect("students.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city) VALUES (?,?,?)",(name,addr,city) )
                con.commit()
                msg = "Record successfully added"

        except Exception as e:
            print(e)
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return render_template("result.html",msg=msg)


@app.route('/deletestu')
@login_required
def deletestu():
    return render_template('delstudent.html')

@app.route('/delrec', methods = ['POST', 'GET'])
def delrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['addr']
            city = request.form['city']      

            with sqlite3.connect("students.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM students WHERE name = (?) AND addr = (?) AND city = (?)" , (name,addr,city) )
                con.commit()
                msg = "Record successfully deleted"

        except Exception as e:
            print(e)
            con.rollback()
            msg = "error in delete operation"
        finally:
            con.close()
            return render_template("delresult.html",msg=msg)

@app.route('/editstu')
@login_required
def editstu():
    return render_template("editstu.html")

@app.route('/editor', methods = ['POST', 'GET'])
def editor():
    if request.method == 'POST':
        try:
            name = request.form.get("name")
            updatename = request.form.get("updatename")
            updateadr = request.form.get("updateadr")
            updatecity = request.form.get("updatecity")

            with sqlite3.connect("students.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE students SET name = ?,  addr = ?, city = ? WHERE name = ?", (updatename, updateadr, updatecity, name) )
                con.commit()
                msg = "Record Successfully Edited"

        except Exception as e:
            print(e)
            con.rollback()
            msg = "error in edit operation"
        finally:
            con.close()
            return render_template("editresults.html", msg=msg)

@app.route('/register')
 
def register():
 
    return render_template('register.html')


@app.route('/')
def home():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("index.html", rows = rows)
    


if __name__ == "__main__":
    app.app_context()
    app.run(debug=True)