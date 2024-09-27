from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u6qortomnaflcybt:Y7A2emdQB293Z2m6W1jq@bz5yijfabuhihultlpar-mysql.services.clever-cloud.com:3306/bz5yijfabuhihultlpar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Cambia esto por una clave segura

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=500.0)  # Saldo inicial en USDT

    def __repr__(self):
        return f'<User {self.username}>'

# Modelo de Transacción
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto = db.Column(db.String(50), nullable=False)  # BTC, ETH, etc.
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # Buy o Sell

    def __repr__(self):
        return f'<Transaction {self.id} - {self.crypto}>'

# Ruta base
@app.route('/')
def base():
    return render_template('home.html')

# Vistas del frontend
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

# Ruta para registrar un nuevo usuario
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

        hashed_password = generate_password_hash(contraseña, method='sha256')
        new_user = User(username=nombre, email=f'{nombre}@example.com', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        password = request.form.get('password')

        if not nombres or not password:
            error = "Por favor, completa ambos campos."
            return render_template('login.html', error=error)

        user = User.query.filter_by(username=nombres).first()
        if user and check_password_hash(user.password, password):
            session['nombres'] = nombres
            access_token = create_access_token(identity={'username': user.username})
            return redirect(url_for('home'))

        error = "Usuario o contraseña incorrectos."
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/trade', methods=['POST'])
@jwt_required()
def api_trade():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

   
    if data['type'] == 'buy':
        cost = float(data['amount']) * float(data['price'])
        if user.balance < cost:
            return jsonify({'message': 'Insufficient funds!'}), 400
        user.balance -= cost
    elif data['type'] == 'sell':
       
        pass

    # Crear una nueva transacción
    new_transaction = Transaction(user_id=user.id, crypto=data['crypto'], amount=data['amount'], price=data['price'], type=data['type'])
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({'message': 'Trade completed successfully!'})

# Ruta para obtener el balance del usuario
@app.route('/balance', methods=['GET'])
@jwt_required()
def get_balance(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    return jsonify({'balance': user.balance})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True)
