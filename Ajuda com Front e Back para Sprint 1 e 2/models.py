import sqlite3
import json
from datetime import datetime

DATABASE = 'database.db'

def get_db():
    """Conecta ao banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('aluno', 'admin')),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de cardápio/refeições
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia_semana TEXT NOT NULL,
            data DATE NOT NULL,
            prato TEXT NOT NULL,
            descricao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de avaliações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            cardapio_id INTEGER NOT NULL,
            nota INTEGER NOT NULL CHECK(nota >= 1 AND nota <= 5),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (cardapio_id) REFERENCES cardapio(id)
        )
    ''')
    
    # Tabela de comentários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            cardapio_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (cardapio_id) REFERENCES cardapio(id)
        )
    ''')
    
    conn.commit()
    
    # Inserir dados de exemplo
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    if cursor.fetchone()[0] == 0:
        # Usuários de exemplo
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo) 
            VALUES (?, ?, ?, ?)
        ''', ('Admin', 'admin@escola.com', 'admin123', 'admin'))
        
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo) 
            VALUES (?, ?, ?, ?)
        ''', ('João Silva', 'joao@escola.com', 'senha123', 'aluno'))
        
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo) 
            VALUES (?, ?, ?, ?)
        ''', ('Maria Santos', 'maria@escola.com', 'senha123', 'aluno'))
        
        # Cardápio de exemplo
        cardapio_exemplo = [
            ('Segunda', '2025-10-27', 'Arroz com Feijão', 'Acompanhado de frango grelhado'),
            ('Terça', '2025-10-28', 'Macarrão à Bolonhesa', 'Com molho caseiro'),
            ('Quarta', '2025-10-29', 'Peixe Grelhado', 'Acompanhado de batata doce'),
            ('Quinta', '2025-10-30', 'Feijoada', 'Servida com arroz e laranja'),
            ('Sexta', '2025-10-31', 'Pizza', 'Sabores variados'),
        ]
        
        for dia, data, prato, descricao in cardapio_exemplo:
            cursor.execute('''
                INSERT INTO cardapio (dia_semana, data, prato, descricao) 
                VALUES (?, ?, ?, ?)
            ''', (dia, data, prato, descricao))
        
        # Avaliações de exemplo
        cursor.execute('''
            INSERT INTO avaliacoes (usuario_id, cardapio_id, nota) 
            VALUES (?, ?, ?)
        ''', (2, 1, 5))
        
        cursor.execute('''
            INSERT INTO avaliacoes (usuario_id, cardapio_id, nota) 
            VALUES (?, ?, ?)
        ''', (3, 1, 4))
        
        cursor.execute('''
            INSERT INTO avaliacoes (usuario_id, cardapio_id, nota) 
            VALUES (?, ?, ?)
        ''', (2, 2, 3))
        
        # Comentários de exemplo
        cursor.execute('''
            INSERT INTO comentarios (usuario_id, cardapio_id, texto) 
            VALUES (?, ?, ?)
        ''', (2, 1, 'Muito saboroso! Recomendo.'))
        
        cursor.execute('''
            INSERT INTO comentarios (usuario_id, cardapio_id, texto) 
            VALUES (?, ?, ?)
        ''', (3, 1, 'Bom, mas poderia ter mais tempero.'))
        
        conn.commit()
    
    conn.close()

def get_usuario_by_email(email):
    """Busca usuário por email"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()
    return dict(usuario) if usuario else None

def get_usuario_by_id(usuario_id):
    """Busca usuário por ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()
    return dict(usuario) if usuario else None

def get_cardapio():
    """Retorna todo o cardápio da semana"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cardapio ORDER BY data')
    cardapio = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cardapio

def get_cardapio_by_id(cardapio_id):
    """Busca refeição específica"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cardapio WHERE id = ?', (cardapio_id,))
    refeicao = cursor.fetchone()
    conn.close()
    return dict(refeicao) if refeicao else None

def add_cardapio(dia_semana, data, prato, descricao):
    """Adiciona nova refeição ao cardápio"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cardapio (dia_semana, data, prato, descricao) 
        VALUES (?, ?, ?, ?)
    ''', (dia_semana, data, prato, descricao))
    conn.commit()
    cardapio_id = cursor.lastrowid
    conn.close()
    return cardapio_id

def update_cardapio(cardapio_id, dia_semana, data, prato, descricao):
    """Atualiza refeição do cardápio"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cardapio 
        SET dia_semana = ?, data = ?, prato = ?, descricao = ? 
        WHERE id = ?
    ''', (dia_semana, data, prato, descricao, cardapio_id))
    conn.commit()
    conn.close()

def delete_cardapio(cardapio_id):
    """Deleta refeição do cardápio"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cardapio WHERE id = ?', (cardapio_id,))
    conn.commit()
    conn.close()

def add_avaliacao(usuario_id, cardapio_id, nota):
    """Adiciona avaliação de refeição"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO avaliacoes (usuario_id, cardapio_id, nota) 
        VALUES (?, ?, ?)
    ''', (usuario_id, cardapio_id, nota))
    conn.commit()
    avaliacao_id = cursor.lastrowid
    conn.close()
    return avaliacao_id

def add_comentario(usuario_id, cardapio_id, texto):
    """Adiciona comentário sobre refeição"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comentarios (usuario_id, cardapio_id, texto) 
        VALUES (?, ?, ?)
    ''', (usuario_id, cardapio_id, texto))
    conn.commit()
    comentario_id = cursor.lastrowid
    conn.close()
    return comentario_id

def get_avaliacoes_por_cardapio(cardapio_id):
    """Retorna todas as avaliações de uma refeição"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, u.nome FROM avaliacoes a 
        JOIN usuarios u ON a.usuario_id = u.id 
        WHERE a.cardapio_id = ?
    ''', (cardapio_id,))
    avaliacoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return avaliacoes

def get_comentarios_por_cardapio(cardapio_id):
    """Retorna todos os comentários de uma refeição"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, u.nome FROM comentarios c 
        JOIN usuarios u ON c.usuario_id = u.id 
        WHERE c.cardapio_id = ?
    ''', (cardapio_id,))
    comentarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comentarios

def get_media_avaliacoes(cardapio_id):
    """Calcula a média de avaliações de uma refeição"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT AVG(nota) as media FROM avaliacoes 
        WHERE cardapio_id = ?
    ''', (cardapio_id,))
    resultado = cursor.fetchone()
    conn.close()
    media = resultado['media'] if resultado['media'] else 0
    return round(media, 2)

