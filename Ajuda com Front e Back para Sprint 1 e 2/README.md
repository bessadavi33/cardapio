# Sistema de Cardápio Escolar

## 📋 Descrição

Sistema web completo para gerenciamento de cardápio escolar, desenvolvido como projeto acadêmico com metodologia Scrum. O sistema permite que alunos consultem o cardápio da semana, avaliem e comentem sobre as refeições, enquanto administradores podem gerenciar o cardápio e visualizar relatórios de avaliações.

## 🎯 Histórias de Usuário Implementadas

### Sprint 1

- **US01**: Como um usuário, eu quero fazer login no sistema com minhas credenciais, para que eu tenha acesso às funcionalidades permitidas para meu perfil.
- **US02**: Como um administrador, eu quero cadastrar e editar o cardápio da semana, informando os pratos de cada dia, para que os alunos saibam o que será servido.
- **US03**: Como um aluno, eu quero consultar o cardápio da semana em uma interface simples, para que eu possa ver as refeições planejadas.

### Sprint 2

- **US04**: Como um aluno, eu quero dar uma avaliação para a refeição de um dia específico, para que a escola saiba meu nível de satisfação.
- **US05**: Como um aluno, eu quero escrever um comentário sobre a refeição, para que eu possa dar um feedback mais detalhado sobre o que gostei ou não.
- **US06**: Como um administrador, eu quero ver a média das avaliações e os comentários para cada prato, para que eu possa identificar pontos de melhoria na merenda.

## 🛠️ Tecnologias Utilizadas

### Back-end
- **Python 3.11**
- **Flask 2.3.3** - Framework web leve
- **Flask-CORS 4.0.0** - Suporte a CORS
- **SQLite** - Banco de dados

### Front-end
- **HTML5** - Estrutura
- **CSS3** - Estilização responsiva
- **JavaScript Puro** - Interatividade (sem dependências externas)

## 📁 Estrutura do Projeto

```
CardapioEscolar/
├── backend/
│   ├── app.py              # Aplicação Flask com rotas da API
│   ├── models.py           # Modelos de banco de dados
│   ├── database.db         # Banco de dados SQLite
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── index.html          # Página principal
│   ├── style.css           # Estilos CSS
│   └── script.js           # Lógica JavaScript
└── README.md               # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)
- Navegador web moderno

### Instalação e Execução

1. **Clone ou extraia o projeto:**
   ```bash
   cd CardapioEscolar
   ```

2. **Instale as dependências do back-end:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Execute o servidor Flask:**
   ```bash
   python app.py
   ```
   
   O servidor estará disponível em `http://localhost:5000`

4. **Acesse a aplicação:**
   - Abra seu navegador e vá para `http://localhost:5000`
   - Use as credenciais de teste fornecidas na tela de login

## 👥 Credenciais de Teste

### Administrador
- **Email:** admin@escola.com
- **Senha:** admin123

### Aluno 1
- **Email:** joao@escola.com
- **Senha:** senha123

### Aluno 2
- **Email:** maria@escola.com
- **Senha:** senha123

## 📡 API REST - Endpoints

### Autenticação
- `POST /api/login` - Fazer login

### Cardápio
- `GET /api/cardapio` - Listar todo o cardápio
- `GET /api/cardapio/<id>` - Obter detalhes de uma refeição
- `POST /api/cardapio` - Criar nova refeição (admin)
- `PUT /api/cardapio/<id>` - Atualizar refeição (admin)
- `DELETE /api/cardapio/<id>` - Deletar refeição (admin)

### Avaliações
- `POST /api/avaliacoes` - Criar avaliação

### Comentários
- `POST /api/comentarios` - Criar comentário

### Relatórios
- `GET /api/relatorio/cardapio/<id>` - Relatório de uma refeição
- `GET /api/relatorio/semana` - Relatório da semana completa

## 🎨 Funcionalidades

### Para Alunos
- ✅ Login seguro
- ✅ Visualizar cardápio da semana
- ✅ Ver detalhes de cada refeição
- ✅ Avaliar refeições (1 a 5 estrelas)
- ✅ Escrever comentários
- ✅ Ver avaliações e comentários de outros alunos

### Para Administradores
- ✅ Login seguro
- ✅ Adicionar refeições ao cardápio
- ✅ Editar refeições existentes
- ✅ Deletar refeições
- ✅ Visualizar relatório de avaliações
- ✅ Ver comentários dos alunos
- ✅ Acompanhar satisfação dos alunos

## 🎯 Metodologia Scrum

Este projeto foi desenvolvido seguindo a metodologia Scrum com:
- **2 Sprints** de desenvolvimento
- **6 Histórias de Usuário** implementadas
- **Reuniões Diárias** para sincronização
- **Reviews e Retrospectives** ao final de cada sprint

## 📊 Banco de Dados

### Tabelas

#### usuarios
- `id` - Identificador único
- `nome` - Nome do usuário
- `email` - Email único
- `senha` - Senha (sem criptografia para demonstração)
- `tipo` - 'aluno' ou 'admin'
- `criado_em` - Data de criação

#### cardapio
- `id` - Identificador único
- `dia_semana` - Dia da semana
- `data` - Data da refeição
- `prato` - Nome do prato
- `descricao` - Descrição do prato
- `criado_em` - Data de criação

#### avaliacoes
- `id` - Identificador único
- `usuario_id` - Referência ao usuário
- `cardapio_id` - Referência à refeição
- `nota` - Nota de 1 a 5
- `criado_em` - Data de criação

#### comentarios
- `id` - Identificador único
- `usuario_id` - Referência ao usuário
- `cardapio_id` - Referência à refeição
- `texto` - Texto do comentário
- `criado_em` - Data de criação

## 🔒 Segurança

**Nota:** Este é um projeto acadêmico de demonstração. Para produção, seria necessário:
- Implementar criptografia de senhas (bcrypt)
- Usar JWT para autenticação
- Validar e sanitizar todas as entradas
- Implementar rate limiting
- Usar HTTPS
- Adicionar autenticação de dois fatores

## 📱 Responsividade

A interface foi desenvolvida com design responsivo, funcionando bem em:
- Desktops (1920px+)
- Tablets (768px a 1024px)
- Smartphones (até 480px)

## 🐛 Tratamento de Erros

- Validação de entrada em todos os formulários
- Mensagens de erro claras para o usuário
- Tratamento de erros de conexão com a API
- Feedback visual para ações do usuário

## 📝 Notas de Desenvolvimento

- O banco de dados é criado automaticamente na primeira execução
- Dados de exemplo são inseridos automaticamente
- CORS está habilitado para facilitar desenvolvimento
- O servidor roda em modo debug (não usar em produção)

## 🎓 Aprendizados

Este projeto demonstra:
- Desenvolvimento full-stack (front-end e back-end)
- Arquitetura REST API
- Manipulação de banco de dados SQLite
- Integração front-end com back-end via fetch API
- Design responsivo e UX
- Metodologia Scrum e histórias de usuário

## 👨‍💻 Autor

Desenvolvido como trabalho acadêmico de Engenharia de Software.

## 📄 Licença

Projeto acadêmico - Uso livre para fins educacionais.

---

**Versão:** 1.0  
**Data:** Outubro 2025  
**Status:** Completo e funcional para apresentação

