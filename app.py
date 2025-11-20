from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# --- CONFIG DATABASE ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, 'warchest_secure.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_FILE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(100), unique=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False) # IN / OUT
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

# --- SECURITY HELPER ---
def get_user():
    token = request.headers.get('Authorization')
    if not token: return None
    return User.query.filter_by(token=token).first()

# --- AUTH ROUTES ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username udah ada!"}), 400
    
    hashed = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        token = str(uuid.uuid4())
        user.token = token
        db.session.commit()
        return jsonify({"token": token, "username": user.username})
    
    return jsonify({"error": "Salah password/username!"}), 401

# --- APP ROUTES ---
@app.route('/api/transactions', methods=['GET'])
def get_trans():
    user = get_user()
    if not user: return jsonify([]), 401
    trans = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.date.desc()).all()
    return jsonify([{
        "id": t.id, "type": t.type, "category": t.category,
        "amount": t.amount, "note": t.note, "date": t.date.strftime('%Y-%m-%d %H:%M')
    } for t in trans])

@app.route('/api/summary', methods=['GET'])
def get_summary():
    user = get_user()
    if not user: return jsonify({"income":0, "expense":0, "balance":0, "survival_days":0}), 401
    
    # 1. Hitung Total Masuk & Keluar
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(user_id=user.id, type='IN').scalar() or 0
    expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(user_id=user.id, type='OUT').scalar() or 0
    balance = income - expense
    
    # 2. LOGIKA SURVIVAL BARU (TIME BASED)
    survival_days = 999 # Default kalau belum ada pengeluaran (Infinity)
    
    # Cari tanggal pengeluaran PERTAMA kali
    first_expense = Transaction.query.filter_by(user_id=user.id, type='OUT').order_by(Transaction.date.asc()).first()
    
    if first_expense and balance > 0:
        # Hitung selisih hari dari transaksi pertama sampai SEKARANG
        days_passed = (datetime.now() - first_expense.date).days
        
        # Minimal pembagi adalah 1 (biar gak error division by zero kalau baru hari ini inputnya)
        if days_passed < 1: days_passed = 1
        
        # Rata-rata pengeluaran per HARI (Real)
        daily_burn_rate = expense / days_passed
        
        if daily_burn_rate > 0:
            survival_days = int(balance / daily_burn_rate)
    
    return jsonify({
        "income": income,
        "expense": expense,
        "balance": balance,
        "survival_days": survival_days
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    user = get_user()
    if not user: return jsonify({}), 401
    res = db.session.query(Transaction.category, db.func.sum(Transaction.amount)).filter_by(user_id=user.id, type='OUT').group_by(Transaction.category).all()
    return jsonify({"labels": [r[0] for r in res], "data": [r[1] for r in res]})

@app.route('/api/add', methods=['POST'])
def add():
    user = get_user()
    if not user: return jsonify({}), 401
    data = request.json
    db.session.add(Transaction(user_id=user.id, type=data['type'], category=data['category'], amount=float(data['amount']), note=data['note']))
    db.session.commit()
    return jsonify({"message": "Saved"})

@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete(id):
    user = get_user()
    if not user: return jsonify({}), 401
    trans = Transaction.query.filter_by(id=id, user_id=user.id).first()
    if trans:
        db.session.delete(trans)
        db.session.commit()
    return jsonify({"message": "Deleted"})

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)