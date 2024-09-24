from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u6qortomnaflcybt:Y7A2emdQB293Z2m6W1jq@bz5yijfabuhihultlpar-mysql.services.clever-cloud.com:3306/bz5yijfabuhihultlpar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()

@app.route('/')
def base():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cripto')
def cripto():
    return render_template('cripto.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/spot')
def spot():
    return render_template('spot.html')

@app.route('/trade')
def trade():
    return render_template('trade.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        password = request.form.get('password')

        if not nombres or not password:
            error = "Por favor, completa ambos campos."
            return render_template('login.html', error=error)

        user = User.query.filter_by(username=nombres).first()
        if user and user.password == password:
            session['nombres'] = nombres
            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre_sign')
        contraseña = request.form.get('password_sign')

        if not nombre or not contraseña:
            flash('Se necesitan nombre y contraseña')
            return redirect(url_for('register'))

        if User.query.filter_by(username=nombre).first():
            flash('El usuario ya existe. Por favor, elija otro nombre de usuario.')
            return redirect(url_for('register'))

        new_user = User(username=nombre, password=contraseña)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
