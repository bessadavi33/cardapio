// ==================== VARIÁVEIS GLOBAIS ====================

const API_URL = 'http://localhost:5001/api';
let usuarioAtual = null;
let refeicaoSelecionada = null;

// ==================== ELEMENTOS DO DOM ====================

const loginScreen = document.getElementById('loginScreen');
const alunoScreen = document.getElementById('alunoScreen');
const adminScreen = document.getElementById('adminScreen');
const loginForm = document.getElementById('loginForm');
const logoutBtn = document.getElementById('logoutBtn');
const logoutBtnAdmin = document.getElementById('logoutBtnAdmin');
const nomeUsuario = document.getElementById('nomeUsuario');
const nomeUsuarioAdmin = document.getElementById('nomeUsuarioAdmin');
const cardapioList = document.getElementById('cardapioList');
const cardapioListAdmin = document.getElementById('cardapioListAdmin');
const refeicaoModal = document.getElementById('refeicaoModal');
const modalTitulo = document.getElementById('modalTitulo');
const modalDetalhes = document.getElementById('modalDetalhes');
const closeModal = document.querySelector('.close');
const cardapioForm = document.getElementById('cardapioForm');
const cancelarEdicaoBtn = document.getElementById('cancelarEdicaoBtn');
const relatorioList = document.getElementById('relatorioList');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// ==================== FUNÇÕES DE ARMAZENAMENTO ====================

function salvarUsuario(usuario) {
    localStorage.setItem('usuarioAtual', JSON.stringify(usuario));
}

function recuperarUsuario() {
    const usuario = localStorage.getItem('usuarioAtual');
    return usuario ? JSON.parse(usuario) : null;
}

function limparUsuario() {
    localStorage.removeItem('usuarioAtual');
}

// ==================== AUTENTICAÇÃO ====================

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, senha })
        });
        
        if (response.ok) {
            usuarioAtual = await response.json();
            salvarUsuario(usuarioAtual); // ← SALVAR NO LOCALSTORAGE
            loginForm.reset();
            mostrarTelaUsuario();
        } else {
            alert('Email ou senha inválidos!');
        }
    } catch (error) {
        console.error('Erro ao fazer login:', error);
        alert('Erro ao conectar com o servidor');
    }
});

logoutBtn.addEventListener('click', logout);
logoutBtnAdmin.addEventListener('click', logout);

function logout() {
    usuarioAtual = null;
    refeicaoSelecionada = null;
    limparUsuario(); // ← LIMPAR DO LOCALSTORAGE
    mostrarTelaLogin();
}

function mostrarTelaLogin() {
    loginScreen.classList.add('active');
    alunoScreen.classList.remove('active');
    adminScreen.classList.remove('active');
}

function mostrarTelaUsuario() {
    loginScreen.classList.remove('active');
    
    if (usuarioAtual.tipo === 'admin') {
        alunoScreen.classList.remove('active');
        adminScreen.classList.add('active');
        nomeUsuarioAdmin.textContent = usuarioAtual.nome;
        carregarCardapioAdmin();
        carregarRelatorio();
    } else {
        adminScreen.classList.remove('active');
        alunoScreen.classList.add('active');
        nomeUsuario.textContent = usuarioAtual.nome;
        carregarCardapio();
    }
}

// ==================== CARDÁPIO (ALUNO) ====================

async function carregarCardapio() {
    try {
        const response = await fetch(`${API_URL}/cardapio`);
        const cardapio = await response.json();
        
        cardapioList.innerHTML = '';
        
        cardapio.forEach(refeicao => {
            const card = document.createElement('div');
            card.className = 'cardapio-card';
            card.innerHTML = `
                <h3>${refeicao.prato}</h3>
                <p class="dia">${refeicao.dia_semana} - ${formatarData(refeicao.data)}</p>
                <p class="descricao">${refeicao.descricao || 'Sem descrição'}</p>
                <div class="stats">
                    <span>
                        <strong>${refeicao.media_avaliacoes.toFixed(1)}</strong>
                        Avaliação
                    </span>
                    <span>
                        <strong>${refeicao.total_avaliacoes}</strong>
                        Votos
                    </span>
                    <span>
                        <strong>${refeicao.total_comentarios}</strong>
                        Comentários
                    </span>
                </div>
            `;
            card.addEventListener('click', () => abrirDetalhesRefeicao(refeicao.id));
            cardapioList.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar cardápio:', error);
    }
}

async function abrirDetalhesRefeicao(cardapioId) {
    try {
        const response = await fetch(`${API_URL}/cardapio/${cardapioId}`);
        const refeicao = await response.json();
        
        refeicaoSelecionada = refeicao;
        
        modalTitulo.textContent = refeicao.prato;
        modalDetalhes.innerHTML = `
            <p><strong>Dia:</strong> ${refeicao.dia_semana} - ${formatarData(refeicao.data)}</p>
            <p><strong>Descrição:</strong> ${refeicao.descricao || 'Sem descrição'}</p>
            <p><strong>Avaliação Média:</strong> ${refeicao.media_avaliacoes.toFixed(1)} ⭐ (${refeicao.total_avaliacoes} votos)</p>
        `;
        
        // Limpar formulário de avaliação
        document.querySelectorAll('input[name="nota"]').forEach(input => input.checked = false);
        
        // Carregar comentários
        carregarComentarios(refeicao.comentarios);
        
        refeicaoModal.classList.add('active');
    } catch (error) {
        console.error('Erro ao carregar detalhes:', error);
    }
}

function carregarComentarios(comentarios) {
    const comentariosList = document.getElementById('comentariosList');
    comentariosList.innerHTML = '';
    
    if (comentarios.length === 0) {
        comentariosList.innerHTML = '<p style="color: #95a5a6; text-align: center;">Nenhum comentário ainda</p>';
        return;
    }
    
    comentarios.forEach(comentario => {
        const item = document.createElement('div');
        item.className = 'comentario-item';
        item.innerHTML = `
            <div class="autor">${comentario.nome}</div>
            <div class="texto">${comentario.texto}</div>
            <div class="data">${formatarData(comentario.criado_em)}</div>
        `;
        comentariosList.appendChild(item);
    });
}

// ==================== AVALIAÇÕES ====================

document.getElementById('enviarAvaliacaoBtn').addEventListener('click', async (e) => {
    e.preventDefault();

    const nota = document.querySelector('input[name="nota"]:checked');
    
    if (!nota) {
        alert('Selecione uma nota!');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/avaliacoes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usuario_id: usuarioAtual.id,
                cardapio_id: refeicaoSelecionada.id,
                nota: parseInt(nota.value)
            })
        });
        
        if (response.ok) {
            alert('Avaliação registrada com sucesso!');
            // ← NÃO RECARREGAR A PÁGINA, APENAS ATUALIZAR OS DADOS
            await carregarCardapio();
            await abrirDetalhesRefeicao(refeicaoSelecionada.id);
        } else {
            alert('Erro ao registrar avaliação');
        }
    } catch (error) {
        console.error('Erro ao enviar avaliação:', error);
        alert('Erro ao conectar com o servidor');
    }
});

// ==================== COMENTÁRIOS ====================

document.getElementById('enviarComentarioBtn').addEventListener('click', async (e) => {
    e.preventDefault();

    const texto = document.getElementById('comentarioTexto').value;
    
    if (!texto.trim()) {
        alert('Escreva um comentário!');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/comentarios`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usuario_id: usuarioAtual.id,
                cardapio_id: refeicaoSelecionada.id,
                texto: texto
            })
        });
        
        if (response.ok) {
            alert('Comentário registrado com sucesso!');
            document.getElementById('comentarioTexto').value = '';
            // ← NÃO RECARREGAR A PÁGINA, APENAS ATUALIZAR OS DADOS
            await abrirDetalhesRefeicao(refeicaoSelecionada.id);
        } else {
            alert('Erro ao registrar comentário');
        }
    } catch (error) {
        console.error('Erro ao enviar comentário:', error);
        alert('Erro ao conectar com o servidor');
    }
});

// ==================== MODAL ====================

closeModal.addEventListener('click', () => {
    refeicaoModal.classList.remove('active');
});

window.addEventListener('click', (e) => {
    if (e.target === refeicaoModal) {
        refeicaoModal.classList.remove('active');
    }
});

// ==================== CARDÁPIO (ADMIN) ====================

let editandoCardapioId = null;

async function carregarCardapioAdmin() {
    try {
        const response = await fetch(`${API_URL}/cardapio`);
        const cardapio = await response.json();
        
        cardapioListAdmin.innerHTML = '';
        
        cardapio.forEach(refeicao => {
            const card = document.createElement('div');
            card.className = 'admin-card';
            card.innerHTML = `
                <div class="admin-card-info">
                    <h4>${refeicao.prato}</h4>
                    <p>${refeicao.dia_semana} - ${formatarData(refeicao.data)}</p>
                    <p>${refeicao.descricao || 'Sem descrição'}</p>
                </div>
                <div class="admin-card-actions">
                    <button class="btn btn-warning" onclick="editarRefeicao(${refeicao.id}, '${refeicao.dia_semana}', '${refeicao.data}', '${refeicao.prato}', '${refeicao.descricao}')">Editar</button>
                    <button class="btn btn-danger" onclick="deletarRefeicao(${refeicao.id})">Deletar</button>
                </div>
            `;
            cardapioListAdmin.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar cardápio:', error);
    }
}

function editarRefeicao(id, dia, data, prato, descricao) {
    editandoCardapioId = id;
    document.getElementById('diaSemana').value = dia;
    document.getElementById('dataRefeicao').value = data;
    document.getElementById('prato').value = prato;
    document.getElementById('descricao').value = descricao;
    cancelarEdicaoBtn.style.display = 'inline-block';
    
    // Scroll para o formulário
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

function cancelarEdicao() {
    editandoCardapioId = null;
    cardapioForm.reset();
    cancelarEdicaoBtn.style.display = 'none';
}

cancelarEdicaoBtn.addEventListener('click', cancelarEdicao);

cardapioForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dia_semana = document.getElementById('diaSemana').value;
    const data = document.getElementById('dataRefeicao').value;
    const prato = document.getElementById('prato').value;
    const descricao = document.getElementById('descricao').value;
    
    try {
        let response;
        
        if (editandoCardapioId) {
            // Atualizar
            response = await fetch(`${API_URL}/cardapio/${editandoCardapioId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    usuario_id: usuarioAtual.id,
                    dia_semana,
                    data,
                    prato,
                    descricao
                })
            });
        } else {
            // Criar
            response = await fetch(`${API_URL}/cardapio`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    usuario_id: usuarioAtual.id,
                    dia_semana,
                    data,
                    prato,
                    descricao
                })
            });
        }
        
        if (response.ok) {
            alert(editandoCardapioId ? 'Refeição atualizada!' : 'Refeição adicionada!');
            cardapioForm.reset();
            editandoCardapioId = null;
            cancelarEdicaoBtn.style.display = 'none';
            await carregarCardapioAdmin();
        }
    } catch (error) {
        console.error('Erro ao salvar refeição:', error);
    }
});

async function deletarRefeicao(id) {
    if (!confirm('Tem certeza que deseja deletar esta refeição?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/cardapio/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usuario_id: usuarioAtual.id
            })
        });
        
        if (response.ok) {
            alert('Refeição deletada!');
            await carregarCardapioAdmin();
        }
    } catch (error) {
        console.error('Erro ao deletar refeição:', error);
    }
}

// ==================== RELATÓRIO ====================

async function carregarRelatorio() {
    try {
        const response = await fetch(`${API_URL}/relatorio/semana`);
        const relatorio = await response.json();
        
        relatorioList.innerHTML = '';
        
        relatorio.forEach(item => {
            const card = document.createElement('div');
            card.className = 'relatorio-card';
            card.innerHTML = `
                <h4>${item.prato}</h4>
                <div class="relatorio-stat">
                    <label>Dia:</label>
                    <span class="value">${item.dia_semana}</span>
                </div>
                <div class="relatorio-stat">
                    <label>Avaliação Média:</label>
                    <span class="value">${item.media_avaliacoes.toFixed(1)} ⭐</span>
                </div>
                <div class="relatorio-stat">
                    <label>Total de Avaliações:</label>
                    <span class="value">${item.total_avaliacoes}</span>
                </div>
                <div class="relatorio-stat">
                    <label>Total de Comentários:</label>
                    <span class="value">${item.total_comentarios}</span>
                </div>
            `;
            relatorioList.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar relatório:', error);
    }
}

// ==================== TABS ====================

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        // Remover classe ativa de todos os botões e abas
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Adicionar classe ativa ao botão clicado e sua aba
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// ==================== FUNÇÕES AUXILIARES ====================

function formatarData(dataString) {
    const data = new Date(dataString);
    return data.toLocaleDateString('pt-BR');
}

// ==================== INICIALIZAÇÃO ====================

// ← RECUPERAR USUÁRIO DO LOCALSTORAGE
usuarioAtual = recuperarUsuario();

if (usuarioAtual) {
    mostrarTelaUsuario();
} else {
    mostrarTelaLogin();
}

