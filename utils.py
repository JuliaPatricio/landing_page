import json
import re

# Função para validar formato de email
def email_valido(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

# Carregar dados do JSON
def carregar_dados():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

# Salvar dados no JSON
def salvar_dados(dados):
    with open('user_data.json', 'w') as f:
        json.dump(dados, f, indent=4)

# Verificar se o email já está cadastrado
def verificar_email_existente(email):
    dados = carregar_dados()
    for user in dados['users']:
        if user['email'] == email:
            return True
    return False

# Verificar se o usuário já existe no login
def verificar_login(username, password):
    dados = carregar_dados()
    for user in dados['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None
