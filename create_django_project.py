import os
import sys
import subprocess
from pathlib import Path

# ========================
# Конфигурация
# ========================

PROJECT_NAME = "portal"
DJANGO_PROJECT_NAME = "config"
APPS_DIR = "apps"
CORE_DIR = "core"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
MEDIA_DIR = "media"

# ========================
# Вспомогательные функции
# ========================

def create_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# ========================
# Содержимое файлов
# ========================

GITIGNORE_CONTENT = """
venv/
__pycache__
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
/media/
/staticfiles/
.env
.env.local
.env.development.local
.env.production.local
"""

README_MD_CONTENT = f"""
# {PROJECT_NAME.capitalize()}

Проект на Django с модульной архитектурой и разделенными настройками.

## Установка

```bash
# Активировать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate     # Windows

# Установить зависимости
pip install -r requirements/dev.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver

#Docker
docker-compose up --build

"""

DOT_ENV_CONTENT = """
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://myuser:mypassword@db:5432/mydb
"""

REQUIREMENTS_BASE_CONTENT = """
Django>=4.2,<5.0
python-dotenv>=1.0.1
dj-database-url>=1.4.2
djangorestframework>=3.14.0
"""

REQUIREMENTS_DEV_CONTENT = """
-r base.txt
psycopg2-binary>=2.9.9
django-debug-toolbar>=4.2.0
flake8>=6.0.0
"""

REQUIREMENTS_PROD_CONTENT = """
-r base.txt
gunicorn>=21.2.0
psycopg2-binary>=2.9.9
whitenoise>=6.4.0
"""

DOCKERFILE_CONTENT = """
FROM python:3.11-slim

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
"""

DOCKER_COMPOSE_YML_CONTENT = """
version: '3.8'

services:
web:
build: .
command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
volumes:
- .:/app
ports:
- "8000:8000"
env_file:
- .env
depends_on:
- db

db:
image: postgres:15-alpine
environment:
POSTGRES_USER: myuser
POSTGRES_PASSWORD: mypassword
POSTGRES_DB: mydb
volumes:
- postgres_data:/var/lib/postgresql/data/
ports:
- "5432:5432"

volumes:
postgres_data:
"""

GITHUB_ACTIONS_CI_YML_CONTENT = """
name: Django CI

on:
push:
branches: [main]
pull_request:
branches: [main]

jobs:
build:
runs-on: ubuntu-latest

steps:
- name: Checkout code
uses: actions/checkout@v3

- name: Set up Python
uses: actions/setup-python@v4
with:
python-version: '3.11'

- name: Install dependencies
run: |
python -m pip install --upgrade pip
pip install -r requirements/dev.txt

- name: Run migrations
run: python manage.py migrate

- name: Run tests
run: python manage.py test

- name: Lint with flake8
run: |
pip install flake8
flake8 .
"""


CONFIG_SETTINGS_BASE_CONTENT = """
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""

CONFIG_SETTINGS_DEVELOPMENT_CONTENT = """
from .base import *

DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug Toolbar
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass
"""

CONFIG_SETTINGS_PRODUCTION_CONTENT = """
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# PostgreSQL
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
"""

CONFIG_URLS_CONTENT = """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api_example.urls')),
]
"""

CONFIG_WSGI_CONTENT = """
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
application = get_wsgi_application()
"""

MANAGE_PY_CONTENT = """
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
"""

API_EXAMPLE_VIEWS_CONTENT = """
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HelloSerializer

class HelloApiView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})

    def post(self, request):
        serializer = HelloSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

API_EXAMPLE_SERIALIZERS_CONTENT = """
from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)
"""

API_EXAMPLE_URLS_CONTENT = """
from django.urls import path
from apps.api_example import views

urlpatterns = [
    path('hello/', views.HelloApiView.as_view(), name='hello'),
]
"""


# ========================
# Основная логика скрипта
# ========================

def main():
    print(f"🚀 Создание структуры проекта: {PROJECT_NAME}")
    project_path = Path(PROJECT_NAME)
    create_dir(project_path)

    # Создаем основные директории
    create_dir(project_path / DJANGO_PROJECT_NAME)
    create_dir(project_path / DJANGO_PROJECT_NAME / "settings")
    create_dir(project_path / APPS_DIR)
    create_dir(project_path / CORE_DIR)
    create_dir(project_path / TEMPLATES_DIR)
    create_dir(project_path / STATIC_DIR)
    create_dir(project_path / MEDIA_DIR)
    create_dir(project_path / "requirements")
    create_dir(project_path / ".github" / "workflows")

    # Создаем файлы
    write_file(project_path / ".gitignore", GITIGNORE_CONTENT)
    write_file(project_path / "README.md", README_MD_CONTENT)
    write_file(project_path / ".env", DOT_ENV_CONTENT)
    write_file(project_path / "requirements" / "base.txt", REQUIREMENTS_BASE_CONTENT)
    write_file(project_path / "requirements" / "dev.txt", REQUIREMENTS_DEV_CONTENT)
    write_file(project_path / "requirements" / "prod.txt", REQUIREMENTS_PROD_CONTENT)
    write_file(project_path / "Dockerfile", DOCKERFILE_CONTENT)
    write_file(project_path / "docker-compose.yml", DOCKER_COMPOSE_YML_CONTENT)
    write_file(project_path / ".github/workflows/ci.yml", GITHUB_ACTIONS_CI_YML_CONTENT)
    write_file(project_path / DJANGO_PROJECT_NAME / "urls.py", CONFIG_URLS_CONTENT)
    write_file(project_path / DJANGO_PROJECT_NAME / "wsgi.py", CONFIG_WSGI_CONTENT)
    write_file(project_path / DJANGO_PROJECT_NAME / "settings" / "base.py", CONFIG_SETTINGS_BASE_CONTENT)
    write_file(project_path / DJANGO_PROJECT_NAME / "settings" / "development.py", CONFIG_SETTINGS_DEVELOPMENT_CONTENT)
    write_file(project_path / DJANGO_PROJECT_NAME / "settings" / "production.py", CONFIG_SETTINGS_PRODUCTION_CONTENT)
    write_file(project_path / "manage.py", MANAGE_PY_CONTENT)
    os.chmod(project_path / "manage.py", 0o755)

    # Создаем __init__.py для модулей
    for init_path in [
        project_path / DJANGO_PROJECT_NAME,
        project_path / DJANGO_PROJECT_NAME / "settings",
        project_path / APPS_DIR,
        project_path / CORE_DIR,
    ]:
        write_file(init_path / "__init__.py", "")

    # Создаем пример DRF приложения
    api_app_dir = project_path / APPS_DIR / "api_example"
    create_dir(api_app_dir)
    create_dir(api_app_dir / "__pycache__")
    write_file(api_app_dir / "__init__.py", "")
    write_file(api_app_dir / "views.py", API_EXAMPLE_VIEWS_CONTENT)
    write_file(api_app_dir / "serializers.py", API_EXAMPLE_SERIALIZERS_CONTENT)
    write_file(api_app_dir / "urls.py", API_EXAMPLE_URLS_CONTENT)

    print("✅ Все файлы успешно созданы.")

    choice = input("Хотите установить зависимости? (y/n): ").strip().lower()
    if choice == 'y':
        print("🔧 Установка зависимостей...")
        venv_path = project_path / "venv"
        print(f"Создаю виртуальное окружение в {venv_path}...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
        pip_path = venv_path / "Scripts" / "pip" if os.name == 'nt' else venv_path / "bin" / "pip"

        print("📦 Установка dev зависимостей...")
        subprocess.check_call([
            str(pip_path), "install", "-r", str(project_path / "requirements" / "dev.txt")
        ])

        print("⚙️ Инициализация проекта Django...")
        print("⚙️ Инициализация проекта Django: пропущена (файлы уже созданы)")
        """venv_bin = venv_path / "Scripts" if os.name == 'nt' else venv_path / "bin"
        django_admin_path = venv_bin / "django-admin"

        # Проверяем, существует ли django-admin
        if not os.path.exists(str(django_admin_path)):
            raise FileNotFoundError(f"Файл не найден: {django_admin_path}")

        # Используем абсолютный путь
        absolute_django_admin = os.path.abspath(str(django_admin_path))

        # Создаём проект
        subprocess.check_call([
            absolute_django_admin, "startproject", DJANGO_PROJECT_NAME, "."], cwd=str(project_path))
        """
        print("✅ Проект готов! Перейдите в папку и активируйте виртуальное окружение.")
    else:
        print("✅ Проект создан без установки зависимостей.")


if __name__ == "__main__":
    main()