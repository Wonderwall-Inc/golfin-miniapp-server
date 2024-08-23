# Setup Instructions:

# Table of Contents

1. [Development Environment Setup](#development-environment-setup)
1. [Project Architecture Setup Steps](#project-architecture-setup-steps)
1. [Directory Structure](#directory-structure)
1. [Code Formatting and Quality Tools](#code-formatting-and-quality-tools)
1. [Commit Rules](#commit-rules)
1. [Docker](#docker)
1. [CI/CD](#ci/cd)


# Development Environment Setup
### Clone Git Repository
```bash
git clone <GIT_REPO_LINK>
cd golfin-miniapp-server
```
### Create Development Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pre-commit install
```
### Run Application
```bash
uvicorn main:app --reload
```

### Run Alembic DB Migration
Add `from app.appName import models` in migrations/env.py and run these command:
```bash
alembic revision --autogenerate
alembic upgrade head
```

### Run Tests
```bash
TESTING=True pytest
```

### Run Docker with a development MySQL Server
```bash
docker-compose -f docker-compose-dev.yaml up --build
```

# Project Architecture Setup Steps

## Directory Structure
	.
	├ app1                           # Application 1 (user)
	│  ├── __init__.py
	│  ├── api                       # Holds all apis
	│  │  └── v1                     # API Version 1
	│  │    ├── __init__.py
	│  │    ├── service.py          # Holds all business logic
	│  │    └── app1.py             # Holds the api routes
	│  ├── schemas.py                # pydantic models
	│  ├── models.py                 # db models
	│  ├── config.py                 # local configs
	│  ├── constants.py
	│  └── utils.py
	├ app2                            # Application 2 (blog)
	│  ├── __init__.py
	│  ├── api                       # Holds all apis
	│  │  └── v1                     # API Version 1
	│  │    ├── __init__.py
	│  │    ├── service.py          # Holds all business logic
	│  │    └── app2.py             # Holds the api routes
	│  ├── schemas.py                # pydantic models
	│  ├── models.py                 # db models
	│  ├── config.py                 # local configs
	│  ├── constants.py
	│  └── utils.py
	├ core                   # Holds all global files
	│  ├──  __init__.py
	│  ├── models.py          # Global db models
	│  ├── config.py          # Global configs
	│  ├── database.py        # db connection related stuff
	│  ├── pagination.py      # global module pagination
	│  ├── constants.py       # Global constants
	│  └── utils.py
	├ tests                   # Holds all the test files
	│  ├── test_app           # Holds all application tests
	│  │  ├── app1            # Application 1
	│  │  │  ├── test_api                     # All App1 API Versions Tests
	│  │  │  │  └── test_v1                   # App1 version 1 API Related Tests
	│  │  │  │    ├── app1_service_test.py    # App1 Buisness Logic Unit Tests
	│  │  │  │    └── app1_test.py            # App1 API Integration Tests
	│  │  │  └── app1_schema_test.py          # App1 Schema Unit Tests
	│  │  ├── app2
	│  │  └── app3
	│  ├── test_core          # Common Test Logics
	│  └── conftest.py        # Autorun Test Configuration
	├── migrations            # Alembic Migrations
	├── .env                  # Holds all environment variables
	├── docker-compose.yaml
	├── Dockerfile
	├── DB.db                 # Local Database
	├── README.md             # Holds project docs
	├── requirements.txt      # Holds all dependency requirements
	├── .pre-commit-config.yaml  # Holds all dependency requirements
	└── main.py               # Main project file


### Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Create Essential Files

```bash
touch .gitignore
touch requirement.txt
touch README.md
```

`.gitignore`
```
#Fast API
__pycache__/
.DS_Store
.Python
build/

*.manifest
*.spec

#Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

### Install essential dependencies
```bash
pip3 install fastapi uvicorn sqlalchemy python-multipart
```

### Run FastAPI App
```bash
uvicorn main:app --reload
```

## Code Formatting and Quality Tools
### Install Formatter
```bash
pip3 install pylint
pip3 install black
black .
```

## Commit Rules
### Pre Commit Hook
```bash
pip3 install pre-commit
touch .pre-commit-config.yaml
pre-commit install
pre-commit run
```

`.pre-commit-config.yaml`
```
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: check-yaml
    -   id: check-json
    -   id: requirements-txt-fixer
    -   id: name-tests-test
-   repo: local
    hooks:
    -   id: pylint
        name: pylint
        entry: pylint -d migrations
        language: system
        types: [python]
        exclude: ^migrations/
        args:
        - --max-line-length=100
        # - --errors-only
        - --disable=W, R
        - --rcfile=.pylintrc
-   repo: local
    hooks:
    -   id: black
        name: black
        entry: black
        language: system
        types: [python]
-   repo: local
    hooks:
    -   id: pytest-check
        name: pytest-check  
        entry: bash -c 'TESTING=True ./venv/bin/python3 -m pytest tests'
        language: system
        pass_filenames: false
        always_run: true

```

## Debugging

Inside of your `.vscode` directory create a `launch.json` file:

`launch.json`

```json
{
	"version": "0.2.0",
	"configurations": [
		{
			"name": "Python: FastAPI",
			"type": "python",
			"request": "launch",
			"module": "uvicorn",
			"args": [
				"main:app",
				"--reload"
			],
			"jinja": true,
			"justMyCode": true
		}
	]
}
```

## Docker

### Docker Compose Dev Environment
`docker-compose-dev.yml`
```yml
services:
  app:
    build: .
    image: arm64v8/python:3.11.6-slim
    container_name: golfin-miniapp-backend
    environment:
      - DB_HOST=db
      - DB_PORT=${DB_PORT}
      - DB_USER=${DB_USER}
      - DB_PASS=${DB_PASS}
      - DB_NAME=${DB_NAME}
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ports:
      - 8000:8000
      - 5678:5678
    volumes:
      - .:/app
    networks:
      - golfin
    depends_on:
      - db
  
  db:
    image: arm64v8/mysql:latest
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: LocalDB
      MYSQL_ROOT_PASSWORD: becareful
    cap_add:
      - SYS_NICE
    ports:
      - 3306:3306
    volumes:
      - MySql-db:/var/lib/mysql
      - ./mysql:/docker-entrypoint-initdb.d
    networks:
      - golfin

networks:
  golfin:
    driver: bridge
volumes:
  MySql-db:
```



`docker-compose.yml`

```yml
services:
  app:
    build: .
    container_name: golfin-miniapp-backend
    environment:
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT}
      - DB_USER=${DB_USER}
      - DB_PASS=${DB_PASS}
      - DB_NAME=${DB_NAME}
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ports:
      - 8000:8000
      - 5678:5678
    volumes:
      - .:/app

  nginx:
    build: ./nginx/.
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

```

Compose Command:
```
docker-compose up
docker-compose down

#For Dev Environment
docker-compose -f docker-compose-dev.yaml up
docker-compose -f docker-compose-dev.yaml down
```

## CI/CD
We are using AWS Code Deploy to achive CI/CD functionality.

Deployment Specification:

`appspec.yml`

```yml
version: 0.0
os: linux
files:
  - source: /
    destination: /home/ec2-user/golfinMiniappBackend
    overwrite: true
file_exists_behavior: OVERWRITE
hooks:
  BeforeInstall:
    - location: scripts/before-install.sh
      timeout: 300
  AfterInstall:
    - location: scripts/after-install.sh
      timeout: 300
  ApplicationStart:
    - location: scripts/app-start.sh
      timeout: 300
  ApplicationStop:
    - location: scripts/app-stop.sh
      timeout: 300
      runas: root
```
`./scripts` folder holds all necessary scripts.