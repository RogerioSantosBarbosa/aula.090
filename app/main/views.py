from flask import render_template
from . import main
from ..models import User  # Importante: Importar o modelo de Usuário

@main.route('/')
def index():
    # Busca todos os usuários no banco de dados
    # O order_by é opcional, mas ajuda a manter a lista organizada alfabeticamente
    users = User.query.order_by(User.username).all()
    
    # Passa a lista de usuários para o template como a variável 'users'
    return render_template('index.html', users=users)
