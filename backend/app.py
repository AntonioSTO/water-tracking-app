# Esta é a versão completa e final do backend/app.py

import os
import jwt
from functools import wraps
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta, date

# --- Inicialização e Configuração ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, expose_headers=["Authorization"], allow_headers=["Authorization", "Content-Type"])
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicialização das Extensões ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# --- Modelos do Banco de Dados ---
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class WaterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumed = db.Column(db.Integer, default=0)
    goal = db.Column(db.Integer, default=2000)
    streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('Usuario', backref=db.backref('water_data', lazy=True, uselist=False))
    last_goal_date = db.Column(db.Date, nullable=True) 
    lifetime_consumed = db.Column(db.Integer, default=0) 


# --- Decorator de Autenticação ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Usuario.query.get(data['sub'])
        except Exception as e: # <-- MUDANÇA AQUI: Capturamos o erro 'e'
            # --- DIAGNÓSTICO FINAL ---
            print(f"[TOKEN-ERRO] Erro ao decodificar token: {e}") 
            return jsonify({'message': 'Token é inválido!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated


# --- Rotas da API ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Este email já está em uso"}), 409
    
    new_user = Usuario(email=data.get('email'))
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    
    # Cria os dados iniciais de água para o novo usuário
    new_water_data = WaterData(user=new_user)
    db.session.add(new_water_data)
    
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@app.route('/login', methods=['POST'])
def login():
    print("\n[LOGIN] Recebida uma tentativa de login.")
    
    # 1. Pega os dados JSON da requisição
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        print("[LOGIN-ERRO] Requisição malformada. Faltando e-mail ou senha.")
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    
    email = data.get('email')
    password = data.get('password')
    print(f"[LOGIN] Tentativa para o e-mail: {email}")

    # 2. Busca o usuário no banco de dados pelo email fornecido
    user = Usuario.query.filter_by(email=email).first()

    # 3. Verifica se o usuário existe E se a senha está correta
    if not user:
        print(f"[LOGIN-ERRO] Usuário com e-mail '{email}' não encontrado no banco de dados.")
        return jsonify({"error": "Credenciais inválidas"}), 401

    print(f"[LOGIN] Usuário encontrado: {user.email}")
    
    password_check_result = user.check_password(password)
    print(f"[LOGIN] Resultado da verificação de senha: {password_check_result}")

    if not password_check_result:
        print("[LOGIN-ERRO] A verificação da senha falhou.")
        return jsonify({"error": "Credenciais inválidas"}), 401

    # 4. Se as credenciais estiverem corretas, gera o token JWT
    print("[LOGIN-SUCESSO] Gerando token JWT.")
    token = jwt.encode({
        'sub': str(user.id),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    # 5. Retorna o token para o cliente
    return jsonify({'access_token': token})

# Rota protegida para pegar os dados do usuário
@app.route('/api/data', methods=['GET'])
@token_required
def get_data(current_user):
    user_data = current_user.water_data
    return jsonify({
        'consumed': user_data.consumed,
        'goal': user_data.goal,
        'streak': user_data.streak,
        'best_streak': user_data.best_streak
    })

# Rota protegida para atualizar os dados do usuário
@app.route('/api/data', methods=['POST'])
@token_required
def update_data(current_user):
    data = request.get_json()
    user_data = current_user.water_data
    today = date.today()

    # Pega os valores antigos antes de atualizar
    previous_consumed = user_data.consumed
    
    # Atualiza os dados com base no que o frontend enviou
    user_data.consumed = data.get('consumed', user_data.consumed)
    user_data.goal = data.get('goal', user_data.goal)

    added_amount = user_data.consumed - previous_consumed
    if added_amount > 0:
        user_data.lifetime_consumed += added_amount

    # --- Lógica de Streak ---
    # Verifica se a meta foi atingida NESTA atualização
    goal_just_reached = (previous_consumed < user_data.goal and user_data.consumed >= user_data.goal)

    # Se a meta foi atingida e ainda não foi registrada hoje...
    if goal_just_reached and user_data.last_goal_date != today:
        user_data.streak += 1
        user_data.last_goal_date = today # Registra a data do feito
        if user_data.streak > user_data.best_streak:
            user_data.best_streak = user_data.streak

    # Atualiza o best_streak (caso tenha sido alterado manualmente ou em outra lógica)
    if user_data.streak > user_data.best_streak:
        user_data.best_streak = user_data.streak

    db.session.commit()
    return jsonify({
        'message': 'Dados atualizados com sucesso!',
        'streak': user_data.streak, # Retorna o streak atualizado
        'best_streak': user_data.best_streak
    })

@app.route('/api/statistics', methods=['GET'])
@token_required
def get_statistics(current_user):
    user_data = current_user.water_data
    registration_date = current_user.created_at.date()
    today = date.today()
    
    # Calcula o número de dias desde o registro
    days_since_registration = (today - registration_date).days + 1

    # Calcula a média diária
    average_daily_consumption = user_data.lifetime_consumed / days_since_registration
    
    return jsonify({
        'lifetime_consumed': user_data.lifetime_consumed,
        'average_daily_consumption': round(average_daily_consumption),
        'days_since_registration': days_since_registration,
        'best_streak': user_data.best_streak,
        'current_goal': user_data.goal
    })

# Não se esqueça de atualizar seu banco de dados!
# Pare o servidor e rode no terminal:
# python
# from app import app, db
# with app.app_context():
#     db.create_all()
# exit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)