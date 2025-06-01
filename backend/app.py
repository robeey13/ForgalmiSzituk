from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
    is_admin = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_admin_password = generate_password_hash('444')
        admin_user = User(username='admin', password=hashed_admin_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin felhasználó létrehozva: username='admin', password='{admin_user.password}'")
    else:
        print(f"Admin felhasználó már létezik: username='admin', password='{admin_user.password}'")


def validate_password(password):
    if len(password) < 8:
        return False, "Jelszónak legalább 8 karakter hosszúnak kell lennie."
    if not re.search(r"[A-Z]", password):
        return False, "Jelszónak tartalmaznia kell legalább egy nagybetűt."
    if not re.search(r"[a-z]", password):
        return False, "Jelszónak tartalmaznia kell legalább egy kisbetűt."
    return True, "Jelszó érvényes."

def validate_username(username):
    if len(username) <= 3:
        return False, "Felhasználónév legalább 4 karakter hosszú kell legyen."
    if username == 'admin':
        return False, "A 'admin' felhasználónév foglalt."
    return True, "Felhasználónév érvényes."
    
def is_admin_user():
    if 'username' not in session:
        return False
    user = User.query.filter_by(username=session['username']).first()
    return user and user.is_admin


@app.route('/')
def index():
    logged_in_user = session.get('username')
    logged_in_user_score = User.query.filter_by(username=logged_in_user).first().score if logged_in_user else 0
    is_admin = is_admin_user()
    return render_template('index.html', logged_in_user_score=logged_in_user_score, logged_in_user=logged_in_user, is_admin=is_admin)

@app.route('/users')
def list_users():
    users = User.query.order_by(User.score.desc()).all()
    logged_in_user = session.get('username')
    logged_in_user_score = User.query.filter_by(username=logged_in_user).first().score if logged_in_user else 0
    is_admin = is_admin_user()
    return render_template('users.html', users=users, logged_in_user_score=logged_in_user_score, logged_in_user=session.get('username'), is_admin=is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
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
            valid1, msg1 = validate_username(username)
            if not valid1:
                error = msg1
            else:
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))





@app.route('/admin')
def admin_panel():
    if not is_admin_user():
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin.html', users=users, logged_in_user=session.get('username'))




@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not is_admin_user():
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)

    if user.username == session['username']:
        return redirect(url_for('admin_panel'))
    
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/make_admin/<int:user_id>', methods=['POST'])
def make_admin(user_id):
    if not is_admin_user():
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/remove_admin/<int:user_id>', methods=['POST'])
def remove_admin(user_id):
    if not is_admin_user():
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.username == session['username']:
        return redirect(url_for('admin_panel'))
    
    user.is_admin = False
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('quiz.html', logged_in_user=session['username'])

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # fúgec, ezt el sem bírom magyarázni

    try:
        adat = request.json.get('adat')

        if adat is None:
            return jsonify({'success': "False", 'error': 'Hibás adat formátum!'}), 400
        
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            return jsonify({'success': "False", 'error': 'Felhasználó nem található!'}), 404
        
        user.score += adat
        db.session.commit()

        return jsonify({'success': "True", 'score': user.score}), 200
    except Exception as e:
        return jsonify({'success': "False", 'error': str(e)}), 500
    
    

if __name__ == '__main__':
    app.run(debug=True)