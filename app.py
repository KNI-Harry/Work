from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisIsSecret'
login_manager = LoginManager(app)
login_manager.login_view="login"


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Forum")
def forum():
    return render_template("forums.html")

@app.route("/Plans")
def plans():
    return render_template("plans.html")

@app.route("/Sign_Up")
def sign_up():
    return render_template("Sign_up.html")

@app.route("/signup_res", methods=["POST", "GET"])
def signup_res():
    if request.method == "POST":

        try:
            Email = request.form.get('Email')
            Username = request.form.get('Username')
            Password = request.form.get('Password')
            
            with sqlite3.connect("People.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO login (Email,Username,Password) VALUES (?,?,?)", (Email,Username,Password))
                conn.commit()
                msg= "You have been added please return to the home page and login"
            
        except Exception as e:
            print(e)
            msg="There was an error adding you into the database"
            conn.rollback()
            
        
        finally:
            conn.close()
            return render_template("signup_res.html", msg=msg)

    





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
    con = sqlite3.connect("People.db")
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
    conn = sqlite3.connect('People.db')
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

if __name__ == "__main__":
    app.app_context()
app.run(debug=True)
