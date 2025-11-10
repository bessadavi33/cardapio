# Conteúdo para Slides - Sistema de Cardápio Escolar

## Slide 1: Capa
**Título:** Sistema de Cardápio Escolar
**Subtítulo:** Desenvolvimento Full-Stack com Scrum
**Informações:** Projeto Acadêmico | Engenharia de Software | 2025

---

## Slide 2: Visão Geral do Projeto
**Título:** O Que É o Sistema de Cardápio Escolar?

O Sistema de Cardápio Escolar é uma aplicação web desenvolvida com metodologia Scrum que permite alunos consultarem o cardápio da semana, avaliarem refeições e deixarem comentários, enquanto administradores gerenciam o cardápio e acompanham a satisfação dos alunos através de relatórios de avaliações.

**Objetivos Principais:**
- Facilitar a comunicação entre escola e alunos sobre refeições
- Coletar feedback dos alunos de forma estruturada
- Permitir que administradores identifiquem pontos de melhoria
- Demonstrar desenvolvimento full-stack em ambiente acadêmico

---

## Slide 3: Histórias de Usuário - Sprint 1
**Título:** Sprint 1: Funcionalidades Fundamentais

**US01 - Autenticação:**
Como um usuário, eu quero fazer login no sistema com minhas credenciais, para que eu tenha acesso às funcionalidades permitidas para meu perfil.

**US02 - Gerenciamento de Cardápio:**
Como um administrador, eu quero cadastrar e editar o cardápio da semana, informando os pratos de cada dia, para que os alunos saibam o que será servido.

**US03 - Consulta de Cardápio:**
Como um aluno, eu quero consultar o cardápio da semana em uma interface simples, para que eu possa ver as refeições planejadas.

---

## Slide 4: Histórias de Usuário - Sprint 2
**Título:** Sprint 2: Feedback e Relatórios

**US04 - Avaliação de Refeições:**
Como um aluno, eu quero dar uma avaliação para a refeição de um dia específico, para que a escola saiba meu nível de satisfação.

**US05 - Comentários Detalhados:**
Como um aluno, eu quero escrever um comentário sobre a refeição, para que eu possa dar um feedback mais detalhado sobre o que gostei ou não.

**US06 - Relatório de Satisfação:**
Como um administrador, eu quero ver a média das avaliações e os comentários para cada prato, para que eu possa identificar pontos de melhoria na merenda.

---

## Slide 5: Arquitetura do Sistema
**Título:** Arquitetura Técnica

**Camadas da Aplicação:**

1. **Front-end (Apresentação)**
   - HTML5 para estrutura semântica
   - CSS3 responsivo para design adaptável
   - JavaScript puro para interatividade (sem dependências)

2. **Back-end (Lógica)**
   - Python com Flask para API REST
   - Endpoints RESTful para todas as operações
   - Validação de dados e controle de acesso

3. **Banco de Dados (Persistência)**
   - SQLite para armazenamento
   - Tabelas normalizadas: usuários, cardápio, avaliações, comentários
   - Relacionamentos entre entidades

---

## Slide 6: Tecnologias Utilizadas
**Título:** Stack Tecnológico

**Back-end:**
- Python 3.11 - Linguagem de programação
- Flask 2.3.3 - Framework web leve
- Flask-CORS 4.0.0 - Suporte a requisições cross-origin
- SQLite - Banco de dados relacional

**Front-end:**
- HTML5 - Markup semântico
- CSS3 - Estilização com grid e flexbox
- JavaScript Vanilla - Sem frameworks externos

**Justificativa:** Stack simples, rápido de desenvolver, fácil de demonstrar e manter em ambiente acadêmico.

---

## Slide 7: Estrutura do Banco de Dados
**Título:** Modelo de Dados

**Tabela: usuarios**
- id (PK), nome, email (UNIQUE), senha, tipo (aluno/admin), criado_em

**Tabela: cardapio**
- id (PK), dia_semana, data, prato, descricao, criado_em

**Tabela: avaliacoes**
- id (PK), usuario_id (FK), cardapio_id (FK), nota (1-5), criado_em

**Tabela: comentarios**
- id (PK), usuario_id (FK), cardapio_id (FK), texto, criado_em

**Relacionamentos:** Um usuário pode fazer múltiplas avaliações e comentários sobre diferentes refeições.

---

## Slide 8: Endpoints da API REST
**Título:** Interface de Comunicação

**Autenticação:**
- POST /api/login - Autenticar usuário

**Cardápio:**
- GET /api/cardapio - Listar cardápio completo
- GET /api/cardapio/<id> - Detalhes de uma refeição
- POST /api/cardapio - Criar refeição (admin)
- PUT /api/cardapio/<id> - Atualizar refeição (admin)
- DELETE /api/cardapio/<id> - Deletar refeição (admin)

**Avaliações e Comentários:**
- POST /api/avaliacoes - Registrar avaliação
- POST /api/comentarios - Registrar comentário

**Relatórios:**
- GET /api/relatorio/semana - Relatório completo da semana
- GET /api/relatorio/cardapio/<id> - Relatório de uma refeição

---

## Slide 9: Interface do Aluno
**Título:** Experiência do Usuário - Aluno

**Funcionalidades:**
1. **Login:** Acesso seguro com email e senha
2. **Visualização do Cardápio:** Cards com informações de cada refeição
3. **Detalhes da Refeição:** Modal com descrição completa
4. **Avaliação:** Sistema de 5 estrelas para cada prato
5. **Comentários:** Campo para deixar feedback detalhado
6. **Feedback Social:** Ver comentários de outros alunos

**Design:** Interface responsiva, intuitiva e acessível em dispositivos móveis e desktops.

---

## Slide 10: Interface do Administrador
**Título:** Experiência do Usuário - Admin

**Funcionalidades:**
1. **Gerenciamento de Cardápio:** Adicionar, editar e deletar refeições
2. **Formulário Estruturado:** Campos para dia, data, prato e descrição
3. **Relatório de Avaliações:** Visualizar média de notas por prato
4. **Análise de Comentários:** Ler feedback detalhado dos alunos
5. **Dashboard:** Visão geral da satisfação da semana

**Controle de Acesso:** Apenas usuários com tipo "admin" podem acessar essas funcionalidades.

---

## Slide 11: Fluxo de Autenticação
**Título:** Como Funciona o Login

1. **Usuário insere credenciais** (email e senha)
2. **Front-end envia requisição POST** para /api/login
3. **Back-end valida credenciais** no banco de dados
4. **Resposta com dados do usuário** (id, nome, tipo)
5. **Front-end armazena dados** em variável global
6. **Interface muda** para tela do aluno ou admin

**Segurança:** Validação no servidor, controle de acesso por tipo de usuário.

---

## Slide 12: Fluxo de Avaliação
**Título:** Como Alunos Avaliam Refeições

1. **Aluno clica em uma refeição** para ver detalhes
2. **Modal abre** com informações completas
3. **Aluno seleciona nota** (1 a 5 estrelas)
4. **Aluno clica em "Enviar Avaliação"**
5. **Front-end envia POST** para /api/avaliacoes
6. **Back-end registra** no banco de dados
7. **Interface atualiza** com nova avaliação

**Feedback:** Mensagem de sucesso e atualização automática da média.

---

## Slide 13: Fluxo de Comentários
**Título:** Como Alunos Deixam Feedback Detalhado

1. **Aluno digita comentário** no campo de texto
2. **Aluno clica em "Enviar Comentário"**
3. **Front-end valida** se o texto não está vazio
4. **Front-end envia POST** para /api/comentarios
5. **Back-end registra** no banco de dados
6. **Comentário aparece** na lista abaixo
7. **Outros alunos podem ver** o feedback

**Dados Capturados:** Texto, usuário, refeição, data/hora.

---

## Slide 14: Relatório do Administrador
**Título:** Dashboard de Satisfação

**Informações Exibidas:**
- Prato e dia da semana
- Média de avaliações (com estrelas)
- Total de votos/avaliações
- Total de comentários
- Lista de comentários com nomes dos alunos

**Casos de Uso:**
- Identificar pratos com baixa avaliação
- Ler sugestões de melhoria dos alunos
- Acompanhar satisfação ao longo do tempo
- Tomar decisões sobre cardápio futuro

---

## Slide 15: Responsividade e Design
**Título:** Acessibilidade em Múltiplos Dispositivos

**Breakpoints Implementados:**
- Desktop (1920px+): Layout em grid com múltiplas colunas
- Tablet (768px-1024px): Ajustes de espaçamento
- Mobile (até 480px): Layout em coluna única, botões otimizados

**Recursos de Design:**
- Cores consistentes e acessíveis
- Tipografia legível
- Feedback visual para interações
- Navegação intuitiva
- Ícones e emojis para melhor compreensão

---

## Slide 16: Dados de Exemplo
**Título:** Sistema Pré-Carregado com Dados

**Usuários Criados:**
- Admin: admin@escola.com / admin123
- Aluno 1: joao@escola.com / senha123
- Aluno 2: maria@escola.com / senha123

**Cardápio da Semana:**
- Segunda: Arroz com Feijão
- Terça: Macarrão à Bolonhesa
- Quarta: Peixe Grelhado
- Quinta: Feijoada
- Sexta: Pizza

**Avaliações e Comentários:** Pré-carregados para demonstração.

---

## Slide 17: Metodologia Scrum
**Título:** Desenvolvimento Ágil

**Sprints Planejadas:**
- Sprint 1 (5-7 dias): Funcionalidades fundamentais (US01, US02, US03)
- Sprint 2 (5-7 dias): Feedback e relatórios (US04, US05, US06)
- Sprint 3 (5-7 dias): Refinamento e testes

**Cerimônias Ágeis:**
- Daily Standup (10 min/dia)
- Sprint Planning (30 min)
- Sprint Review (30 min)
- Sprint Retrospective (30 min)

**Métricas:** Velocidade, burndown chart, taxa de conclusão de histórias.

---

## Slide 18: Benefícios do Scrum
**Título:** Por Que Scrum Para Este Projeto?

1. **Equipe Pequena:** Estrutura leve com papéis claros (PO, SM, Dev)
2. **Entregas Incrementais:** Protótipos funcionais a cada sprint
3. **Feedback Precoce:** Ajustes rápidos baseados em feedback
4. **Flexibilidade:** Adaptação a mudanças de requisitos
5. **Visibilidade:** Burndown charts e métricas claras
6. **Colaboração:** Comunicação diária e síncrona
7. **Qualidade:** Testes e revisões contínuas

**Resultado:** Projeto entregue no prazo com alta qualidade.

---

## Slide 19: Desafios e Soluções
**Título:** Obstáculos Superados

**Desafio 1: Integração Front-end e Back-end**
- Solução: CORS habilitado, API REST bem documentada

**Desafio 2: Validação de Dados**
- Solução: Validação no servidor e no cliente

**Desafio 3: Segurança de Autenticação**
- Solução: Controle de acesso por tipo de usuário

**Desafio 4: Responsividade**
- Solução: CSS Grid e Flexbox com media queries

**Desafio 5: Dados Realistas**
- Solução: Seed de dados automático no banco

---

## Slide 20: Lições Aprendidas
**Título:** Conhecimentos Adquiridos

1. **Full-Stack Development:** Integração completa de front-end e back-end
2. **API REST:** Design de endpoints e comunicação HTTP
3. **Banco de Dados:** Modelagem relacional e SQL
4. **JavaScript Vanilla:** Manipulação do DOM sem frameworks
5. **CSS Responsivo:** Design adaptável para múltiplos dispositivos
6. **Metodologia Ágil:** Prática real de Scrum
7. **Versionamento:** Git para controle de código
8. **Testes:** Validação manual e testes de API

---

## Slide 21: Possíveis Melhorias Futuras
**Título:** Roadmap Pós-Projeto

**Curto Prazo:**
- Criptografia de senhas com bcrypt
- Autenticação com JWT tokens
- Validação mais robusta de entrada
- Testes automatizados (unit e integration)

**Médio Prazo:**
- Autenticação de dois fatores
- Histórico de cardápios
- Filtros e busca avançada
- Notificações por email

**Longo Prazo:**
- App mobile (React Native)
- Integração com sistema de gestão escolar
- Analytics avançado
- Machine learning para recomendações

---

## Slide 22: Demonstração Ao Vivo
**Título:** Vamos Testar o Sistema!

**Demonstração Prática:**
1. Fazer login como aluno
2. Visualizar cardápio da semana
3. Abrir detalhes de uma refeição
4. Deixar avaliação (5 estrelas)
5. Escrever comentário
6. Fazer login como admin
7. Visualizar relatório de satisfação
8. Adicionar nova refeição ao cardápio

**Observações:** Sistema responsivo, dados em tempo real, interface intuitiva.

---

## Slide 23: Conclusão
**Título:** Resumo do Projeto

**Objetivos Alcançados:**
- ✅ Desenvolvimento full-stack completo
- ✅ Implementação de todas as 6 histórias de usuário
- ✅ Interface responsiva e intuitiva
- ✅ API REST funcional e documentada
- ✅ Banco de dados estruturado
- ✅ Aplicação pronta para demonstração

**Impacto:** Sistema prático que melhora a comunicação entre escola e alunos, coletando feedback valioso para melhorias contínuas.

---

## Slide 24: Perguntas e Discussão
**Título:** Dúvidas?

**Tópicos para Discussão:**
- Decisões arquiteturais
- Implementação técnica
- Metodologia Scrum aplicada
- Possíveis extensões do projeto
- Feedback sobre a apresentação

**Contato:** [Informações de contato do grupo]

