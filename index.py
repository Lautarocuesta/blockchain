from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        password = request.form.get('password')

        if not nombres or not password:
            flash('Se necesitan nombre y contraseña')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=nombres).first()
        if user and user.password == password:
            session['nombres'] = nombres
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')

    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
