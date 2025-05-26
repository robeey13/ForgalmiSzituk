from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'FREAKING_SECRET'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()


def validate_password(password):
    if len(password) < 8:
        return False, "Jelszónak legalább 8 karakter hosszúnak kell lennie."
    if not re.search(r"[A-Z]", password):
        return False, "Jelszónak tartalmaznia kell legalább egy nagybetűt."
    if not re.search(r"[a-z]", password):
        return False, "Jelszónak tartalmaznia kell legalább egy kisbetűt."
    return True, "Jelszó érvényes."


@app.route('/')
def index():
    logged_in_user = session.get('username')
    return render_template('index.html', logged_in_user=logged_in_user)

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users, logged_in_user=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Hibás adatok!')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Felhasználónév már létezik!'
        else:
            valid, msg = validate_password(password)
            if not valid:
                error = msg
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)