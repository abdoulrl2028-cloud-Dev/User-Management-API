# User Management API - Django

Uma API RESTful completa para gerenciamento de usuários construída com Django e Django REST Framework.

## Características

- ✅ Autenticação de usuários
- ✅ CRUD completo de usuários
- ✅ Alterar senha
- ✅ Desativar conta
- ✅ Validação de dados robusta
- ✅ CORS habilitado
- ✅ Admin customizado
- ✅ Suporte a PostgreSQL
- ✅ Pronto para deploy em Render, Railway e AWS

## Estrutura do Projeto

```
django_api/
├── core/
│   ├── __init__.py
│   ├── settings.py        # Configurações do Django
│   ├── urls.py            # URLs principais
│   └── wsgi.py            # Configuração WSGI
├── users/
│   ├── __init__.py
│   ├── admin.py           # Configuração do admin
│   ├── apps.py            # Configuração da app
│   ├── models.py          # Modelo CustomUser
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # ViewSets
│   ├── permissions.py     # Permissões customizadas
│   └── urls.py            # URLs da app
├── manage.py
├── requirements.txt
├── Procfile               # Para Heroku/Render
├── runtime.txt            # Versão do Python
└── .env.example           # Template de variáveis de ambiente
```

## Instalação Local

### Pré-requisitos
- Python 3.11+
- pip

### Passos

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd django_api
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor**
```bash
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/api/`

## Endpoints da API

### Autenticação
- `POST /api/users/` - Criar novo usuário
- `GET /api/users/me/` - Obter dados do usuário autenticado

### Gerenciamento de Usuários
- `GET /api/users/` - Listar todos os usuários
- `GET /api/users/{id}/` - Obter detalhes de um usuário
- `PUT /api/users/{id}/` - Atualizar dados do usuário
- `PATCH /api/users/{id}/` - Atualização parcial
- `DELETE /api/users/{id}/` - Deletar usuário

### Ações Especiais
- `POST /api/users/{id}/change_password/` - Alterar senha
- `POST /api/users/{id}/deactivate/` - Desativar conta

## Exemplo de Uso

### Criar novo usuário
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@example.com",
    "password": "senhaSegura123!",
    "password2": "senhaSegura123!",
    "first_name": "João",
    "last_name": "Silva"
  }'
```

### Obter perfil do usuário
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Basic $(echo -n 'joao:senhaSegura123!' | base64)"
```

### Alterar senha
```bash
curl -X POST http://localhost:8000/api/users/1/change_password/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'joao:senhaSegura123!' | base64)" \
  -d '{
    "old_password": "senhaSegura123!",
    "new_password": "novaSenha456!",
    "new_password2": "novaSenha456!"
  }'
```

## Configuração para Banco de Dados PostgreSQL

1. Descomente as linhas do PostgreSQL em `core/settings.py`
2. Instale o driver PostgreSQL:
```bash
pip install psycopg2-binary
```
3. Configure as variáveis de ambiente:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=user_api
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

## Deploy em Render

### Passo 1: Prepare o repositório
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Passo 2: No dashboard do Render
1. Clique em "New +" → "Web Service"
2. Conecte seu repositório GitHub
3. Configure as seguintes variáveis de ambiente:
   - `SECRET_KEY`: Uma chave secreta segura
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: seu-app.render.com
   - `DATABASE_URL`: PostgreSQL URL (Render fornece)

4. Build Command: `pip install -r requirements.txt && python manage.py migrate`
5. Start Command: `gunicorn core.wsgi`

## Deploy em Railway

### Passo 1: Instale a CLI do Railway
```bash
npm install -g @railway/cli
```

### Passo 2: Login e deploy
```bash
railway login
railway init
railway up
```

### Passo 3: Configure variáveis de ambiente
```bash
railway variables set SECRET_KEY=sua-chave-secreta
railway variables set DEBUG=False
```

## Deploy em AWS

### Opção 1: AWS Elastic Beanstalk

1. Instale a CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.11 user-management-api --region us-east-1
```

3. Create environment:
```bash
eb create production
```

4. Deploy:
```bash
eb deploy
```

### Opção 2: AWS EC2 + RDS

1. Crie uma instância EC2 (Ubuntu 20.04 LTS)
2. Conecte via SSH
3. Clone o repositório
4. Siga os passos de instalação local
5. Configure PostgreSQL RDS
6. Use Nginx + Gunicorn + Supervisor para gerenciar o processo

## Variáveis de Ambiente Importantes

```env
SECRET_KEY=sua-chave-secreta-gerada
DEBUG=False                          # Em produção
ALLOWED_HOSTS=seu-dominio.com
DATABASE_URL=postgresql://...       # Para PostgreSQL
CORS_ALLOWED_ORIGINS=https://seu-frontend.com
```

## Testes

```bash
python manage.py test
```

## Estrutura de Modelos

### CustomUser
- `id` - ID único
- `username` - Nome de usuário único
- `email` - Email único
- `password` - Senha criptografada
- `first_name` - Primeiro nome
- `last_name` - Sobrenome
- `phone` - Telefone (opcional)
- `bio` - Biografia (opcional)
- `avatar` - Foto de perfil (opcional)
- `is_active` - Conta ativa
- `is_verified` - Email verificado
- `created_at` - Data de criação
- `updated_at` - Data de atualização

## Segurança

- ✅ Senhas criptografadas com PBKDF2
- ✅ CSRF protection
- ✅ XSS protection
- ✅ Validação de dados robusta
- ✅ SSL/TLS em produção
- ✅ CORS configurável

## Licença

MIT

## Suporte

Para mais informações, visite a documentação do Django:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
