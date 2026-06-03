# Personal Min API

Uma API Django REST robusta para gerenciamento de entradas de diário com autenticação JWT, permissões de grupos e controle de acesso.

## 📋 Sobre o Projeto

Personal Min API é uma aplicação backend que permite:
- ✅ Registro e autenticação de usuários com JWT
- ✅ Gerenciamento de entradas de diário privadas/públicas
- ✅ Permissões baseadas em grupos (grupo "Editor" para leitura)
- ✅ Logout com token blacklist
- ✅ Informações do usuário autenticado

## 🚀 Requisitos

- Python 3.8+
- Django 6.0+
- Django REST Framework
- djangorestframework-simplejwt

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd personal-min-api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
python manage.py migrate
```

### 5. Crie o grupo "Editor"
```bash
python manage.py create_editor_group
```

### 6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

## 🏃 Como Executar

```bash
python manage.py runserver
```

A API estará disponível em: http://localhost:8000

## 📚 Documentação dos Endpoints

### 🔐 Autenticação

#### 1. Registro de Novo Usuário
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "seu_usuario",
  "email": "seu@email.com",
  "password": "sua_senha_forte"
}
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "username": "seu_usuario",
  "email": "seu@email.com"
}
```

#### 2. Login (Obter Tokens)
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha_forte"
}
```

**Resposta (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Atualizar Access Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "seu_refresh_token"
}
```

**Resposta (200 OK):**
```json
{
  "access": "novo_access_token"
}
```

#### 4. Obter Usuário Autenticado
```http
GET /api/auth/me/
Authorization: Bearer seu_access_token
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "username": "seu_usuario",
  "email": "seu@email.com",
  "date_joined": "2026-06-03T10:30:00Z"
}
```

#### 5. Logout (Invalidar Token)
```http
POST /api/auth/logout/
Authorization: Bearer seu_access_token
Content-Type: application/json

{
  "refresh": "seu_refresh_token"
}
```

**Resposta (200 OK):**
```json
{
  "detail": "Logout realizado com sucesso."
}
```

### 📔 Entradas de Diário

#### 1. Listar Entradas (Autenticado)
```http
GET /api/entries/
Authorization: Bearer seu_access_token
```

**Comportamento:**
- Usuários comuns: veem apenas suas entradas
- Membros do grupo "Editor": veem todas as entradas

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "author": "seu_usuario",
    "title": "Meu Primeiro Dia",
    "content": "Hoje foi um ótimo dia...",
    "mood": "happy",
    "is_public": false,
    "created_at": "2026-06-03T10:30:00Z"
  }
]
```

#### 2. Criar Nova Entrada
```http
POST /api/entries/
Authorization: Bearer seu_access_token
Content-Type: application/json

{
  "title": "Dia Especial",
  "content": "Conteúdo da entrada...",
  "mood": "happy",
  "is_public": false
}
```

**Moods disponíveis:** `happy`, `neutral`, `sad`

**Resposta (201 Created):**
```json
{
  "id": 1,
  "author": "seu_usuario",
  "title": "Dia Especial",
  "content": "Conteúdo da entrada...",
  "mood": "happy",
  "is_public": false,
  "created_at": "2026-06-03T10:30:00Z"
}
```

#### 3. Obter uma Entrada Específica
```http
GET /api/entries/1/
Authorization: Bearer seu_access_token
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "author": "seu_usuario",
  "title": "Dia Especial",
  "content": "Conteúdo da entrada...",
  "mood": "happy",
  "is_public": false,
  "created_at": "2026-06-03T10:30:00Z"
}
```

#### 4. Atualizar Entrada
```http
PUT /api/entries/1/
Authorization: Bearer seu_access_token
Content-Type: application/json

{
  "title": "Dia Especial - Atualizado",
  "content": "Novo conteúdo...",
  "mood": "neutral",
  "is_public": true
}
```

**Resposta (200 OK):** Entrada atualizada

#### 5. Deletar Entrada
```http
DELETE /api/entries/1/
Authorization: Bearer seu_access_token
```

**Resposta (204 No Content)**

#### 6. Listar Entradas Públicas (Sem Autenticação)
```http
GET /api/journal/public/
```

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "author": "seu_usuario",
    "title": "Dia Especial",
    "content": "Conteúdo...",
    "mood": "happy",
    "created_at": "2026-06-03T10:30:00Z"
  }
]
```

## 👥 Sistema de Grupos

### Criar Usuário Editor

**Via Django Shell:**
```python
python manage.py shell

from django.contrib.auth.models import User, Group
user = User.objects.get(username='seu_usuario')
editor_group = Group.objects.get(name='Editor')
user.groups.add(editor_group)
```

**Via Django Admin:** http://localhost:8000/admin/

### Permissões do Grupo "Editor"
- ✅ Ler todas as entradas (somente leitura)
- ❌ Não pode editar
- ❌ Não pode deletar
- ✅ Pode ver suas próprias entradas normalmente

## 🔒 Segurança

### Headers Obrigatórios
```
Authorization: Bearer <seu_access_token>
Content-Type: application/json
```

### Ciclo de Vida do Token
- **Access Token:** 15 minutos
- **Refresh Token:** 7 dias
- **Logout:** Invalida o refresh token via blacklist

## 📂 Estrutura do Projeto

```
personal-min-api/
├── accounts/              # App de autenticação
│   ├── models.py
│   ├── views.py          # RegisterView, CurrentUserView, LogoutView
│   ├── serializers.py    # RegisterSerializer, UserSerializer
│   └── migrations/
├── journal/              # App de diário
│   ├── models.py         # JournalEntry
│   ├── views.py          # JournalEntryViewSet, PublicJournalEntryViewSet
│   ├── serializers.py    # JournalEntrySerializer, PublicJournalEntrySerializer
│   ├── permissions.py    # IsOwnerOrEditorReadOnly
│   ├── management/       # Management commands
│   │   └── commands/
│   │       └── create_editor_group.py
│   └── migrations/
├── core/                 # Configurações principais
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'django'"
**Solução:** Ative o ambiente virtual
```bash
source venv/bin/activate
```

### Erro: "Database connection refused"
**Solução:** Execute as migrações
```bash
python manage.py migrate
```

### Erro: "Grupo 'Editor' não encontrado"
**Solução:** Execute o comando de criação
```bash
python manage.py create_editor_group
```

## 🚀 Deployment

Para deployment em produção:

1. Configure as variáveis de ambiente em `.env`
2. Ajuste `DEBUG = False` em `settings.py`
3. Configure `ALLOWED_HOSTS`
4. Use um banco de dados robusto (PostgreSQL)
5. Configure CORS se necessário
6. Use um servidor WSGI (Gunicorn, uWSGI)

## 📝 Licença

MIT

## 👨‍💻 Autor

Desenvolvido com ❤️

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
