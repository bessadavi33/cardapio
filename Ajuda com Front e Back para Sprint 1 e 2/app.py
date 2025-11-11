from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from models import (
    init_db, get_usuario_by_email, get_usuario_by_id, get_cardapio, 
    get_cardapio_by_id, add_cardapio, update_cardapio, delete_cardapio,
    add_avaliacao, add_comentario, get_avaliacoes_por_cardapio, 
    get_comentarios_por_cardapio, get_media_avaliacoes
)

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Inicializar banco de dados na primeira execução
init_db()

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/api/login', methods=['POST'])
def login():
    """US01: Login de usuário"""
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    usuario = get_usuario_by_email(email)
    
    if not usuario or usuario['senha'] != senha:
        return jsonify({'erro': 'Email ou senha inválidos'}), 401
    
    return jsonify({
        'id': usuario['id'],
        'nome': usuario['nome'],
        'email': usuario['email'],
        'tipo': usuario['tipo']
    }), 200

# ==================== ROTAS DE CARDÁPIO ====================

@app.route('/api/cardapio', methods=['GET'])
def obter_cardapio():
    """US03: Consultar cardápio da semana"""
    cardapio = get_cardapio()
    
    # Enriquecer com avaliações e comentários
    for refeicao in cardapio:
        refeicao['media_avaliacoes'] = get_media_avaliacoes(refeicao['id'])
        refeicao['total_avaliacoes'] = len(get_avaliacoes_por_cardapio(refeicao['id']))
        refeicao['total_comentarios'] = len(get_comentarios_por_cardapio(refeicao['id']))
    
    return jsonify(cardapio), 200

@app.route('/api/cardapio/<int:cardapio_id>', methods=['GET'])
def obter_refeicao(cardapio_id):
    """Obter detalhes de uma refeição específica"""
    refeicao = get_cardapio_by_id(cardapio_id)
    
    if not refeicao:
        return jsonify({'erro': 'Refeição não encontrada'}), 404
    
    refeicao = dict(refeicao)
    refeicao['avaliacoes'] = get_avaliacoes_por_cardapio(cardapio_id)
    refeicao['comentarios'] = get_comentarios_por_cardapio(cardapio_id)
    refeicao['media_avaliacoes'] = get_media_avaliacoes(cardapio_id)
    
    return jsonify(refeicao), 200

@app.route('/api/cardapio', methods=['POST'])
def criar_cardapio():
    """US02: Admin cadastrar refeição no cardápio"""
    data = request.json
    usuario_id = data.get('usuario_id')
    
    # Verificar se é admin
    usuario = get_usuario_by_id(usuario_id)
    if not usuario or usuario['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem adicionar cardápio'}), 403
    
    dia_semana = data.get('dia_semana')
    data_refeicao = data.get('data')
    prato = data.get('prato')
    descricao = data.get('descricao', '')
    
    if not all([dia_semana, data_refeicao, prato]):
        return jsonify({'erro': 'Campos obrigatórios: dia_semana, data, prato'}), 400
    
    cardapio_id = add_cardapio(dia_semana, data_refeicao, prato, descricao)
    
    return jsonify({
        'id': cardapio_id,
        'mensagem': 'Refeição adicionada com sucesso'
    }), 201

@app.route('/api/cardapio/<int:cardapio_id>', methods=['PUT'])
def editar_cardapio(cardapio_id):
    """US02: Admin editar refeição do cardápio"""
    data = request.json
    usuario_id = data.get('usuario_id')
    
    # Verificar se é admin
    usuario = get_usuario_by_id(usuario_id)
    if not usuario or usuario['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem editar cardápio'}), 403
    
    refeicao = get_cardapio_by_id(cardapio_id)
    if not refeicao:
        return jsonify({'erro': 'Refeição não encontrada'}), 404
    
    dia_semana = data.get('dia_semana', refeicao['dia_semana'])
    data_refeicao = data.get('data', refeicao['data'])
    prato = data.get('prato', refeicao['prato'])
    descricao = data.get('descricao', refeicao['descricao'])
    
    update_cardapio(cardapio_id, dia_semana, data_refeicao, prato, descricao)
    
    return jsonify({'mensagem': 'Refeição atualizada com sucesso'}), 200

@app.route('/api/cardapio/<int:cardapio_id>', methods=['DELETE'])
def deletar_cardapio(cardapio_id):
    """Admin deletar refeição do cardápio"""
    data = request.json
    usuario_id = data.get('usuario_id')
    
    # Verificar se é admin
    usuario = get_usuario_by_id(usuario_id)
    if not usuario or usuario['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem deletar cardápio'}), 403
    
    refeicao = get_cardapio_by_id(cardapio_id)
    if not refeicao:
        return jsonify({'erro': 'Refeição não encontrada'}), 404
    
    delete_cardapio(cardapio_id)
    
    return jsonify({'mensagem': 'Refeição deletada com sucesso'}), 200

# ==================== ROTAS DE AVALIAÇÕES ====================

@app.route('/api/avaliacoes', methods=['POST'])
def criar_avaliacao():
    """US04: Aluno avaliar refeição"""
    data = request.json
    usuario_id = data.get('usuario_id')
    cardapio_id = data.get('cardapio_id')
    nota = data.get('nota')
    
    if not all([usuario_id, cardapio_id, nota]):
        return jsonify({'erro': 'Campos obrigatórios: usuario_id, cardapio_id, nota'}), 400
    
    if not (1 <= nota <= 5):
        return jsonify({'erro': 'Nota deve estar entre 1 e 5'}), 400
    
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    refeicao = get_cardapio_by_id(cardapio_id)
    if not refeicao:
        return jsonify({'erro': 'Refeição não encontrada'}), 404
    
    avaliacao_id = add_avaliacao(usuario_id, cardapio_id, nota)
    
    return jsonify({
        'id': avaliacao_id,
        'mensagem': 'Avaliação registrada com sucesso'
    }), 201

# ==================== ROTAS DE COMENTÁRIOS ====================

@app.route('/api/comentarios', methods=['POST'])
def criar_comentario():
    """US05: Aluno escrever comentário sobre refeição"""
    data = request.json
    usuario_id = data.get('usuario_id')
    cardapio_id = data.get('cardapio_id')
    texto = data.get('texto')
    
    if not all([usuario_id, cardapio_id, texto]):
        return jsonify({'erro': 'Campos obrigatórios: usuario_id, cardapio_id, texto'}), 400
    
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    refeicao = get_cardapio_by_id(cardapio_id)
    if not refeicao:
        return jsonify({'erro': 'Refeição não encontrada'}), 404
    
    comentario_id = add_comentario(usuario_id, cardapio_id, texto)
    
    return jsonify({
        'id': comentario_id,
        'mensagem': 'Comentário registrado com sucesso'
    }), 201

# ==================== ROTAS DE RELATÓRIOS ====================

@app.route('/api/relatorio/cardapio/<int:cardapio_id>', methods=['GET'])
def relatorio_cardapio(cardapio_id):
    """US06: Admin visualizar média de avaliações e comentários"""
    refeicao = get_cardapio_by_id(cardapio_id)
    
    if not refeicao:
        return jsonify({'erro': 'Refeição não encontrada'}), 404
    
    avaliacoes = get_avaliacoes_por_cardapio(cardapio_id)
    comentarios = get_comentarios_por_cardapio(cardapio_id)
    media = get_media_avaliacoes(cardapio_id)
    
    return jsonify({
        'refeicao': dict(refeicao),
        'media_avaliacoes': media,
        'total_avaliacoes': len(avaliacoes),
        'total_comentarios': len(comentarios),
        'avaliacoes': avaliacoes,
        'comentarios': comentarios
    }), 200

@app.route('/api/relatorio/semana', methods=['GET'])
def relatorio_semana():
    """Relatório completo da semana para admin"""
    cardapio = get_cardapio()
    
    relatorio = []
    for refeicao in cardapio:
        relatorio.append({
            'id': refeicao['id'],
            'dia_semana': refeicao['dia_semana'],
            'prato': refeicao['prato'],
            'media_avaliacoes': get_media_avaliacoes(refeicao['id']),
            'total_avaliacoes': len(get_avaliacoes_por_cardapio(refeicao['id'])),
            'total_comentarios': len(get_comentarios_por_cardapio(refeicao['id']))
        })
    
    return jsonify(relatorio), 200

# ==================== ROTA PARA SERVIR FRONTEND ====================

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Servir arquivos estáticos"""
    return send_from_directory('../frontend', filename)

# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Rota não encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
