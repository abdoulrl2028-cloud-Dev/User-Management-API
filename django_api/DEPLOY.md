# GUIA COMPLETO DE DEPLOY

## 1. DEPLOY EM RENDER.COM

### Passo a Passo:

#### 1. Prepare o repositório Git
```bash
cd django_api
git init
git add .
git commit -m "Initial Django User API"
git push origin main
```

#### 2. No Dashboard do Render (https://dashboard.render.com)

1. Clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Preencha as informações:
   - **Name**: `user-management-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn core.wsgi`
   - **Instance Type**: `Free` (ou pago)

#### 3. Configure Variáveis de Ambiente

No dashboard do Render, vá para **"Environment"** e adicione:

```
SECRET_KEY=gere-uma-chave-com-uuid-ou-secrets
DEBUG=False
ALLOWED_HOSTS=seu-app-nome.render.com
DATABASE_URL=postgresql://usuario:senha@host:5432/nome_db
CORS_ALLOWED_ORIGINS=https://seu-frontend.render.com
```

#### 4. Gere uma SECRET_KEY segura (Python):
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 5. Deploy Automático

- Todo push para `main` faz deploy automático
- Você pode acompanhar em **"Logs"**

---

## 2. DEPLOY EM RAILWAY.APP

### Passo a Passo:

#### 1. Instale a CLI do Railway
```bash
npm install -g @railway/cli
# ou com Homebrew (Mac)
brew install railway
```

#### 2. Login e Deploy
```bash
railway login
cd django_api
railway init
```

#### 3. Selecione as opções:
- **Create a new project**: `user-management-api`
- **Select services**: `None` (adicionaremos depois)

#### 4. Gere um arquivo railway.json:
```json
{
  "buildCommand": "pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput",
  "startCommand": "gunicorn core.wsgi",
  "PORT": 8000
}
```

#### 5. Configure variáveis de ambiente
```bash
railway variables set SECRET_KEY="sua-chave-secreta"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="seu-app.railway.app"
railway variables set DATABASE_URL="postgresql://..."
```

#### 6. Deploy
```bash
railway up
```

#### 7. Veja o status
```bash
railway status
```

---

## 3. DEPLOY EM AWS ELASTIC BEANSTALK

### Passo a Passo:

#### 1. Instale a CLI do EB
```bash
pip install awsebcli
```

#### 2. Configure AWS Credentials
```bash
aws configure
```

Você precisa de:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`

#### 3. Initialize Elastic Beanstalk
```bash
cd django_api
eb init -p python-3.11 user-management-api --region us-east-1
```

#### 4. Crie um arquivo `.ebextensions/django.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: core.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: core.settings
    PYTHONPATH: /var/app/current:$PYTHONPATH

commands:
  01_migrate:
    command: "python manage.py migrate"
    leader_only: true
  02_collectstatic:
    command: "python manage.py collectstatic --noinput"

packages:
  yum:
    postgresql15-devel: []
```

#### 5. Crie o ambiente
```bash
eb create production --single --instance-type t3.micro
```

#### 6. Configure variáveis de ambiente
```bash
eb setenv \
  SECRET_KEY="sua-chave-secreta" \
  DEBUG="False" \
  ALLOWED_HOSTS="seu-app.elasticbeanstalk.com" \
  DATABASE_URL="postgresql://usuario:senha@seu-rds.amazonaws.com:5432/user_api"
```

#### 7. Deploy
```bash
eb deploy
```

#### 8. Veja logs
```bash
eb logs
```

#### 9. Abra a aplicação
```bash
eb open
```

---

## 4. DEPLOY EM AWS EC2 + RDS (Forma Manual)

### Passo 1: Crie uma instância EC2

1. Acesse AWS Console → EC2
2. Launch Instance
3. Escolha: **Ubuntu 22.04 LTS** (t3.micro free tier)
4. Crie/selecione um Security Group que permita:
   - SSH (porta 22) - seu IP
   - HTTP (porta 80) - 0.0.0.0/0
   - HTTPS (porta 443) - 0.0.0.0/0

### Passo 2: Conecte via SSH
```bash
ssh -i seu-chave.pem ubuntu@seu-ip-publica
```

### Passo 3: Atualize o sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql-client nginx git
```

### Passo 4: Clone e configure a aplicação
```bash
cd /home/ubuntu
git clone seu-repositorio
cd User-Management-API/django_api

# Crie virtual env
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### Passo 5: Crie arquivo .env
```bash
nano .env
```

Adicione:
```
SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,seu-ip
DATABASE_URL=postgresql://usuario:senha@seu-rds-endpoint:5432/user_api
```

### Passo 6: Configure Gunicorn

Crie `/home/ubuntu/gunicorn_config.py`:
```python
workers = 4
worker_class = 'sync'
bind = '127.0.0.1:8000'
accesslog = '/home/ubuntu/User-Management-API/django_api/logs/access.log'
errorlog = '/home/ubuntu/User-Management-API/django_api/logs/error.log'
```

### Passo 7: Configure Supervisor (para manter rodando)
```bash
sudo apt install -y supervisor
```

Crie `/etc/supervisor/conf.d/django.conf`:
```ini
[program:django-api]
directory=/home/ubuntu/User-Management-API/django_api
command=/home/ubuntu/User-Management-API/django_api/venv/bin/gunicorn \
  core.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 4

autostart=true
autorestart=true
user=ubuntu
```

### Passo 8: Configure Nginx (Reverse Proxy)

Crie `/etc/nginx/sites-available/django-api`:
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/User-Management-API/django_api/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/User-Management-API/django_api/media/;
    }
}
```

### Passo 9: Ative Nginx
```bash
sudo ln -s /etc/nginx/sites-available/django-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Passo 10: Execute migrations
```bash
cd /home/ubuntu/User-Management-API/django_api
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Passo 11: Inicie os serviços
```bash
sudo systemctl restart supervisor
sudo systemctl status supervisor
```

### Passo 12: HTTPS com Let's Encrypt (Certbot)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

---

## 5. DEPLOY COM DOCKER (Local ou em servidor)

### Build e Run Local:
```bash
docker build -t user-api:latest .
docker run -p 8000:8000 user-api:latest
```

### Com Docker Compose:
```bash
docker-compose up -d
```

---

## VERIFICAÇÃO FINAL

Após o deploy, verifique:

1. **API raiz:**
```bash
curl https://seu-dominio.com/api/
```

2. **Criar usuário:**
```bash
curl -X POST https://seu-dominio.com/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "email": "teste@example.com",
    "password": "SenhaSegura123!",
    "password2": "SenhaSegura123!"
  }'
```

3. **Admin:**
```
https://seu-dominio.com/admin/
```

---

## TROUBLESHOOTING

### Erro 502 Bad Gateway
- Verifique se o servidor Django está rodando
- Logs: `eb logs` ou `sudo journalctl -u supervisor`

### Erro de conexão com banco de dados
- Verifique DATABASE_URL
- Confirme que o banco de dados está rodando
- Verifique inbound rules do RDS

### Erro 404 em arquivos estáticos
- Execute: `python manage.py collectstatic --noinput`
- Verifique STATIC_ROOT em settings.py

---

## VARIÁVEIS DE AMBIENTE ESSENCIAIS

```
SECRET_KEY                  # Gerada com get_random_secret_key()
DEBUG                       # False em produção
ALLOWED_HOSTS              # Domínios permitidos
DATABASE_URL               # postgresql://...
CORS_ALLOWED_ORIGINS       # URLs do frontend
```

---

## BACKUP E MONITORAMENTO

### Backup do Banco de Dados (PostgreSQL)
```bash
pg_dump -U usuario -h host nome_db > backup.sql
```

### Restaurar
```bash
psql -U usuario -h host nome_db < backup.sql
```

### Monitorar Logs
- Render: Dashboard → Logs
- Railway: `railway logs`
- EB: `eb logs --stream`
- EC2: `/var/log/` ou `supervisor`

---

Pronto! Seu Django User Management API está pronto para deploy! 🚀
