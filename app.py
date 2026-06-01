import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from langchain_groq import ChatGroq
from load_dotenv import load_dotenv
from langchain_core.messages import SystemMessage
app = Flask(__name__)
app.secret_key = os.urandom(24)
load_dotenv(dotenv_path="/home/parupiro/Desktop/Python/flask_projects/keys.env") #Substitua pelo diretório do seu environment
API_KEY = os.environ["GROQ_API_KEY"]

# Configuração da API Groq
llm = ChatGroq (
    model_name="llama-3.3-70b-versatile", # Definimos o nome exato do modelo solicitado
    groq_api_key= API_KEY
)
# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect('conversas.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def salvar_mensagem(session_id, role, content):
    conn = sqlite3.connect('conversas.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO mensagens (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (session_id, role, content, datetime.now()))
    conn.commit()
    conn.close()

def obter_historico(session_id, limit=50):
    conn = sqlite3.connect('conversas.db')
    c = conn.cursor()
    c.execute('''
        SELECT role, content FROM mensagens
        WHERE session_id = ?
        ORDER BY timestamp DESC LIMIT ?
    ''', (session_id, limit))
    rows = c.fetchall()
    conn.close()
    # Retornar na ordem cronológica (mais antigo primeiro)
    historico = []
    for role, content in reversed(rows):
        historico.append({"role": role, "content": content})
    return historico

def chamar_groq(mensagens_usuario):
    return llm.invoke(mensagens_usuario).content

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"error": "Mensagem vazia"}), 400
    
    # Salvar mensagem do usuário
    salvar_mensagem(session_id, 'user', user_message)
    
    # Obter histórico recente (últimas 10 trocas)
    historico = obter_historico(session_id)
    # Usar apenas as últimas 10 mensagens para contexto
    historico_recente = historico[-10:] if len(historico) > 10 else historico
    # Preparar mensagens para a API
    mensagens_api = historico_recente + [{"role": "user", "content": user_message}]
    
    # Chamar Groq
    resposta = chamar_groq(mensagens_api)
    
    # Salvar resposta do assistente
    salvar_mensagem(session_id, 'assistant', resposta)
    
    return jsonify({"response": resposta})
@app.route('/history', methods=['POST'])
def get_history():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    historico = obter_historico(session_id)
    return jsonify({"history": historico})
if __name__ == '__main__':
    app.run(debug=True)
