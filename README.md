# 💰 Assistente Financeiro com Inteligência Artificial

Um assistente inteligente projetado para simplificar a gestão e o registo financeiro pessoal. Através de uma interface web interativa em formato de chat, o sistema processa mensagens em linguagem natural utilizando Inteligência Artificial para identificar transações, categorizar despesas/receitas e persistir os dados automaticamente em base de dados local.

---

## 🚀 Funcionalidades

- **Registo em Linguagem Natural:** Interpretação de mensagens de texto sobre despesas e receitas.
- **Categorização Automática com IA:** Identificação inteligente de tipo (receita/despesa), valor, categoria e forma de pagamento.
- **Armazenamento Seguro:** Persistência relacional local com SQLite (`financeiro.db`).
- **Interface Web Conversacional:** Chat dinâmico (`chat.html`) para interação direta com o assistente.
- **Isolamento de Credenciais:** Configurações e chaves de API gerenciadas por variáveis de ambiente (`.env`).

---

## 🏗️ Arquitetura do Sistema

```mermaid
graph TD
    User([Usuário]) -->|Mensagem de texto| UI[Interface Web / chat.html]
    UI -->|Requisição HTTP / JSON| App[Backend Python / app.py]
    App -->|Prompt de Análise| AI[Módulo de IA / ai_service.py]
    AI -->|Dados Estruturados Extraídos| App
    App -->|Persistência / Consultas SQL| DB[(Base de Dados / db.py - SQLite)]
    App -->|Resposta formatada| UI
🔄 Fluxo de Processamento de Transações
Snippet de código
sequenceDiagram
    autonumber
    actor User as Usuário
    participant UI as Interface (chat.html)
    participant API as Servidor (app.py)
    participant IA as Serviço de IA (ai_service.py)
    participant DB as SQLite (db.py)

    User->>UI: "Gastei R$ 45 no almoço no cartão de crédito"
    UI->>API: POST /mensagem { texto: "..." }
    API->>IA: Processar e extrair dados da transação
    IA-->>API: JSON estruturado { tipo, valor, categoria, pagamento }
    API->>DB: registrar_transacao(...)
    DB-->>API: Confirmação de persistência
    API-->>UI: Resposta do assistente confirmando o registo
    UI-->>User: Exibe mensagem no chat
📁 Estrutura do Projeto
Plaintext
assistente-financeiro-ia/
├── app.py             # Servidor web e rotas da aplicação
├── ai_service.py      # Integração com os modelos de Inteligência Artificial
├── db.py              # Camada de dados e operações SQLite
├── chat.html          # Interface web de interação do chat
├── requirements.txt   # Dependências do projeto
├── .env.example       # Modelo de variáveis de ambiente
├── .gitignore         # Ficheiros ignorados pelo Git
└── README.md          # Documentação do repositório
🛠️ Tecnologias Utilizadas
Linguagem: Python 3.10+

Persistência de Dados: SQLite

Frontend: HTML5, CSS3, JavaScript (Fetch API)

Modelos de IA: Integração via serviços de LLM

Gerenciador de Dependências: pip

⚙️ Pré-requisitos e Instalação
Clone o repositório:

Bash
git clone [https://github.com/RomarioGamaa/assistente-financeiro-IA.git](https://github.com/RomarioGamaa/assistente-financeiro-IA.git)
cd assistente-financeiro-IA
Crie e ative um ambiente virtual:

Bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
Instale as dependências:

Bash
pip install -r requirements.txt
Configure as variáveis de ambiente:
Duplique o ficheiro .env.example e renomeie para .env:

Bash
cp .env.example .env
Adicione as suas credenciais e chaves de API necessárias no .env.

Inicie a aplicação:

Bash
python app.py
Acesse a interface no seu navegador através do endereço indicado no terminal (normalmente http://localhost:5000 ou http://localhost:8000).

🛡️ Boas Práticas e Segurança
Credenciais: O ficheiro .env nunca deve ser submetido ao repositório.

Base de Dados: O ficheiro SQLite local (financeiro.db) deve permanecer listado no .gitignore para preservar dados locais e de teste fora do controlo de versões.


---

