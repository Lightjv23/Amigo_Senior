# 👴 Amigo Sênior

Um chatbot inteligente desenvolvido para prover acompanhamento e suporte conversacional para idosos, utilizando a API do **Groq** com o modelo **Llama 3.3-70b-versatile** e técnicas avançadas de engenharia de prompts como **Few-shot Prompting**.

## 🎯 Problema Social

**Amigo Sênior** foi concebido para combater o isolamento social e a solidão em idosos, oferecendo:

- ✅ **Companhia digital 24/7**: Um assistente sempre disponível para conversas
- ✅ **Suporte emocional**: Diálogos empáticos e personalizados
- ✅ **Informações acessíveis**: Respostas em linguagem simples e clara
- ✅ **Histórico de conversas**: Manutenção de contexto entre sessões
- ✅ **Interface intuitiva**: Design pensado para facilidade de uso

A solidão em idosos está associada a diversos problemas de saúde física e mental. Este projeto usa IA para proporcionar interação significativa e combater esses desafios.

---

## 🏗️ Arquitetura e Fluxo de Dados

### Diagrama de Fluxo Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                      FLUXO AMIGO SÊNIOR                              │
└─────────────────────────────────────────────────────────────────────┘

     USUÁRIO (Frontend)
           │
           ├──► Interface Web (HTML/CSS/JavaScript)
           │
           ▼
  ┌────────────────────┐
  │ Input do Usuário   │
  │  (chat.html)       │
  └────────────────────┘
           │
           │ Fetch POST: /send
           │ Payload: { message, session_id }
           │
           ▼
  ┌────────────────────────────────────────┐
  │    SERVIDOR (Flask - app.py)           │
  │                                        │
  │  1. Recebe mensagem do usuário        │
  │  2. Valida entrada                    │
  │  3. Salva em SQLite                   │
  │                                        │
  │  → salvar_mensagem()                  │
  │    (role: 'user', content)            │
  └────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────┐
  │   CAMADA DE CONTEXTO CONVERSACIONAL    │
  │                                        │
  │  1. Recupera histórico recente         │
  │     (últimas 10 mensagens)             │
  │  2. Monta array de mensagens           │
  │     com contexto anterior              │
  │                                        │
  │  → obter_historico()                  │
  │    (session_id, limit=50)             │
  │                                        │
  │  → Prepara: historico_recente + nova  │
  └────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────┐
  │   PROCESSAMENTO DE PROMPTS (Few-Shot)  │
  │                                        │
  │  Mensagens formatadas como:            │
  │  [                                     │
  │    {"role": "user",      "content"...} │
  │    {"role": "assistant", "content"...} │
  │    {"role": "user",      "content"...} │
  │  ]                                     │
  │                                        │
  │  ✨ Few-Shot: Histórico fornece       │
  │     exemplos de conversa ao modelo    │
  └────────────────────────────────────────┘
           │
           │ Invoke LLM
           │
           ▼
  ┌─────────────────────────────────────────────┐
  │    GROQ API - llama-3.3-70b-versatile      │
  │                                             │
  │  • Processamento via Cloud Groq             │
  │  • Latência ultra-baixa                     │
  │  • Modelo otimizado para performance        │
  │                                             │
  │  URL: https://api.groq.com/openai/...       │
  │  Modelo: llama-3.3-70b-versatile            │
  │  Auth: GROQ_API_KEY (env var)               │
  └─────────────────────────────────────────────┘
           │
           │ Resposta JSON
           │
           ▼
  ┌────────────────────────────────────────┐
  │   PROCESSAMENTO DA RESPOSTA            │
  │                                        │
  │  1. Recebe content da IA               │
  │  2. Valida resposta                    │
  │  3. Salva em SQLite                    │
  │                                        │
  │  → salvar_mensagem()                  │
  │    (role: 'assistant', resposta)      │
  └────────────────────────────────────────┘
           │
           │ JSON Response
           │ { "response": "..." }
           │
           ▼
  ┌────────────────────────────────────────┐
  │    FRONTEND - Renderização            │
  │                                        │
  │  1. Recebe resposta via JSON           │
  │  2. Renderiza na UI                    │
  │  3. Atualiza scroll para nova msg      │
  │  4. Re-ativa input para próxima msg    │
  └────────────────────────────────────────┘
           │
           ▼
     👤 USUÁRIO VIRA MENSAGEM
        (Ciclo se repete)
```

### Componentes Principais

| Componente | Descrição |
|-----------|-----------|
| **Frontend** | HTML/CSS/JavaScript - Interface conversacional |
| **Backend** | Flask (Python) - Orquestração e roteamento |
| **LLM** | Groq API com Llama 3.3-70b | 
| **Database** | SQLite - Persistência de histórico |
| **Sessões** | localStorage (JavaScript) + DB |

---

## 🔧 Justificativa Tecnológica

### Por que Groq API?

**Decisão Principal: Utilizar API Groq em vez de alternativas**

#### ✅ Vantagens da Escolha

1. **Velocidade Extrema**
   - Groq oferece latência de ~50-200ms (vs 1-5s em OpenAI/Anthropic)
   - Essencial para conversas fluidas com idosos
   - Experiência de usuário superior

2. **Custo-Benefício**
   - Preço significativamente mais baixo que OpenAI
   - Modelo Llama 3.3-70b (open-source) via Groq
   - Viável para projetos sem fins lucrativos

3. **Modelo Llama 3.3-70b Versatile**
   - 70 bilhões de parâmetros
   - Excelente para tarefas de conversação natural
   - Treino em dados multilíngues (PT-BR)
   - Otimizado para inferência rápida em Groq

4. **Privacidade Aprimorada**
   - Menor risco comparado a armazenamento local em GPU
   - Conformidade com LGPD (Lei Geral de Proteção de Dados)
   - Dados não utilizados para treinamento de modelos Groq

#### Comparação com Alternativas

| Aspecto | Groq | OpenAI | Ollama Local | Anthropic |
|--------|------|--------|--------------|-----------|
| **Latência** | ⚡ 50-200ms | 🟡 1-5s | 🔴 5-30s | 🟡 1-4s |
| **Custo** | 💚 Baixo | 💰 Alto | 💚 Grátis (GPU) | 💰 Alto |
| **Qualidade** | ✅ Excelente | ✅ Superior | ✅ Boa | ✅ Excelente |
| **Privacidade** | 🟢 Média | 🔴 Baixa* | 🟢 Alta | 🟢 Média |
| **Facilidade** | ✅ Simples | ✅ Simples | 🟡 Complexa | ✅ Simples |

*OpenAI pode usar dados para treinamento (verificar configuração)

### Stack Tecnológico

```
Frontend Layer:
├── HTML5 (templates/chat.html)
├── CSS3 (static/style.css) - Design responsivo
└── JavaScript vanilla - Sem dependências pesadas

Backend Layer:
├── Flask 2.x - Framework web leve e rápido
├── LangChain - Integração com Groq
├── ChatGroq - Wrapper oficial Groq
└── Python 3.8+

Database Layer:
└── SQLite3 - Persistência local simples

API Integration:
├── Groq Cloud API
├── REST endpoints (/send, /history)
└── JSON para comunicação

Deployment:
└── Flask development server (escalável com Gunicorn)
```

---

## 🧠 Técnicas Aplicadas de IA

### 1. **Few-Shot Prompting** ⭐ Principal

#### O que é?

Few-shot prompting fornece **exemplos anteriores de conversas** ao modelo para que ele compreenda o padrão de comportamento esperado. O modelo aprende pelo contexto histórico.

#### Implementação no Amigo Sênior

```python
# Arquivo: app.py, linhas 81-89

# Obter histórico recente (últimas 10 trocas)
historico = obter_historico(session_id)
historico_recente = historico[-10:] if len(historico) > 10 else historico

# Preparar mensagens para a API
mensagens_api = historico_recente + [{"role": "user", "content": user_message}]

# Chamar Groq - O modelo recebe histórico como "exemplos"
resposta = chamar_groq(mensagens_api)
```

**Como funciona:**

```
Primeira Mensagem (Cold Start):
User: "Oi, como você está?"

Segunda Mensagem (Few-Shot aplicado):
[
  {"role": "user", "content": "Oi, como você está?"},        ← Exemplo 1
  {"role": "assistant", "content": "Olá! Estou bem! 😊"},     ← Exemplo 1
  {"role": "user", "content": "Qual é seu nome?"}             ← Nova pergunta
]

O modelo vê que:
- Ele deve responder de forma amigável
- Deve manter tom conversacional
- Pode usar emojis
- Deve ser empático
```

#### Vantagens

- ✅ **Consistência**: Modelo mantém personalidade ao longo da conversa
- ✅ **Contexto**: Lembra de tópicos discutidos anteriormente
- ✅ **Adaptação**: Aprende o "tom" esperado pelo histórico
- ✅ **Sem Fine-Tuning**: Não requer retrainamento do modelo

### 2. **Persistência de Histórico com SQLite**

Cada conversa é armazenada para:
- Recuperar contexto em sessões futuras
- Manter continuidade de tópicos
- Permitir análise de padrões de conversa

```python
# Estrutura do banco de dados
CREATE TABLE mensagens (
    id INTEGER PRIMARY KEY,
    session_id TEXT,              ← Identifica usuário/sessão
    role TEXT,                    ← "user" ou "assistant"
    content TEXT,                 ← Corpo da mensagem
    timestamp DATETIME            ← Rastreamento temporal
)
```

### 3. **Gestão de Contexto Limitado**

Para evitar:
- ❌ Custos excessivos (muitos tokens)
- ❌ Perda de foco (contexto muito longo)
- ❌ Confusão do modelo

**Implementação:**

```python
# Usar apenas as últimas 10 mensagens para contexto
historico_recente = historico[-10:] if len(historico) > 10 else historico
```

**Tradeoff:**
- Conversas muito longas (200+ mensagens) perdem contexto antigo
- Solução futura: Implementar RAG com embeddings

---

## 🚀 Técnicas NÃO Aplicadas (Por Quê?)

### ❌ RAG (Retrieval-Augmented Generation)

**Por que não?**
- Escopo atual: Conversação livre, não busca em base conhecimento
- Adição futura: Poderia integrar FAQs de cuidados com saúde

**Como seria:**
```
Pergunta: "Como tratar pressão alta?"
     ↓
[RAG] Buscar artigos sobre hipertensão em base vetorial
     ↓
[LLM] Gerar resposta baseada em documentos recuperados
```

### ❌ Chain-of-Thought (CoT)

**Por que não?**
- Conversação casual: não requer "passo-a-passo"
- Poderia ser adicionado para:
  - Questões matemáticas
  - Resolução de problemas complexos

**Exemplo de uso futuro:**
```
Pergunta: "Se tenho R$ 100 e gasto 30%, quanto sobra?"

Chain-of-Thought:
1. Total inicial: R$ 100
2. Percentual gasto: 30%
3. Valor gasto: 100 × 0.30 = R$ 30
4. Sobra: 100 - 30 = R$ 70
```

### ❌ Fine-Tuning do Modelo

**Por que não?**
- Llama 3.3-70b já é excelente para conversa
- Fine-tuning requereria:
  - Dataset de milhares de exemplos
  - GPU dedicada (caro)
  - Expertise em ML avançado

**Quando seria útil:**
- Dataset próprio de 10k+ exemplos de conversas
- Necessidade de "voz" muito específica

---

## 📊 Fluxo de Processamento Detalhado

### Etapa 1: Entrada do Usuário

```html
<!-- templates/chat.html -->
<input type="text" id="user-input" placeholder="Digite sua mensagem...">
<button id="send-btn">Enviar</button>
```

### Etapa 2: Validação e Armazenamento

```python
# app.py - Route /send
@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:  # Validação
        return jsonify({"error": "Mensagem vazia"}), 400
    
    # Persistir no SQLite
    salvar_mensagem(session_id, 'user', user_message)
```

### Etapa 3: Construção de Contexto (Few-Shot)

```python
# Recupera últimas 10 mensagens
historico = obter_historico(session_id)
historico_recente = historico[-10:]

# Formato para API: Lista de dicts com role/content
mensagens_api = historico_recente + [
    {"role": "user", "content": user_message}
]

# Exemplo de estrutura:
# [
#   {"role": "assistant", "content": "Olá! Sou o Amigo Sênior..."},
#   {"role": "user", "content": "Como você está?"},
#   {"role": "assistant", "content": "Estou bem, obrigado!"},
#   {"role": "user", "content": "Qual é o clima hoje?"}  ← Nova pergunta
# ]
```

### Etapa 4: Inferência com Groq

```python
def chamar_groq(mensagens_usuario):
    # LangChain abstrai a comunicação com Groq
    return llm.invoke(mensagens_usuario).content

# Internamente:
# POST https://api.groq.com/openai/v1/chat/completions
# {
#   "model": "llama-3.3-70b-versatile",
#   "messages": [... historico + nova pergunta ...],
#   "temperature": 0.7 (padrão)
# }
```

### Etapa 5: Armazenamento da Resposta

```python
resposta = chamar_groq(mensagens_api)
salvar_mensagem(session_id, 'assistant', resposta)
```

### Etapa 6: Retorno ao Frontend

```python
return jsonify({"response": resposta})
```

### Etapa 7: Renderização na UI

```javascript
// templates/chat.html
const data = await response.json();
addMessage('assistant', data.response);
```

---

## 📁 Estrutura de Arquivos

```
Amigo_Senior/
├── app.py                 # Backend Flask + Groq integration
├── requirements.txt       # Dependências Python
├── conversas.db          # SQLite database (gerado em runtime)
├── README.md             # Esta documentação
│
├── templates/
│   └── chat.html         # Interface conversacional (HTML+JS)
│
└── static/
    └── style.css         # Estilos e responsividade
```

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
# Python 3.8+
python --version

# Pip
pip --version
```

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Lightjv23/Amigo_Senior.git
cd Amigo_Senior

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt
```

### Configuração da API

```bash
# 1. Obtenha uma chave Groq em: https://console.groq.com
#    (Criar conta e gerar API key)

# 2. Crie arquivo .env na raiz (NÃO versionar!)
echo "GROQ_API_KEY=sua_chave_aqui" > .env

# Ou configure via variável de ambiente:
export GROQ_API_KEY="sua_chave_aqui"
```

### Execução

```bash
# Inicie o servidor Flask
python app.py

# Acesse em seu navegador:
# http://localhost:5000
```

---

## 🔐 Segurança e Privacidade

- ✅ **LGPD Compliant**: Dados armazenados localmente em SQLite
- ✅ **API Key**: Nunca commit em repositório (usar .env)
- ✅ **Session IDs**: Único por usuário (localStorage)
- ⚠️ **TLS**: Implementar em produção
- ⚠️ **Rate Limiting**: Adicionar proteção contra abuse

---

## 📈 Melhorias Futuras

- [ ] Implementar RAG com documentos sobre saúde para idosos
- [ ] Adicionar análise de sentimento das conversas
- [ ] Integrar with reminders e agendamentos
- [ ] Suporte a múltiplos idiomas
- [ ] Dashboard para cuidadores/familiares
- [ ] Integração com wearables (monitorar bem-estar)
- [ ] Fine-tuning em dataset de conversas com idosos
- [ ] Chain-of-Thought para resolução de problemas

---

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -am 'Adiciona X'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

---

## 📜 Licença

Este projeto é licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

---

## 👨‍💻 Desenvolvedor

**Lightjv23** - Desenvolvedor e Pesquisador em IA para Bem-estar Social

---

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no GitHub ou entre em contato através das discussões do repositório.

---

**Amigo Sênior** - Tecnologia com Coração 💜
