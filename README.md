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
git clone git@github.com:Wonderwall-Inc/golfin-miniapp-server.git
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

### Run the migration on the local
```bash
sh ./scripts/alembic-init.sh
```

### Clean up the docker and docker container
```bash
sh ./scripts/docker-cleanup.sh
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

## Models

### User Model

```py
 """
    Represents an user entity and defines the structure of the "user" table in the database.

    Fields:
    - id: An integer column representing the primary key of the "user" table.
    - username: A string column representing the username on the telegram.
    - telegram_id: A string column representing the telegram_id on the telegram.
    - token_balance: A integer column representing the total token amount as ton / eth from user coins.
    - is_active: A boolean column representing if the user is inactive or active per every 3 months.
    - is_premium: A boolean column showing if the user is premium telegram user.
    - in_game_items: A dictionary column showing the items which belong to the user.
    - wallet_address: A string column showing the user ton wallet address on telegram.
    - created_at: A datetime column showing the time when the user was created.
    - updated_at: A datetime column showing the time when the user was updated.
    - skin: A string column showing the skin of the user #affect the reward
    - chat_id: A string column showing which chat does the user belong to with bot  #marketing
    - location: A string column showing where is the user. #marketing  #prefecture
    - nationality: A string column showing which conuntry the user belong to. #marketing
    - age: A string column showing the age of the user. #marketing
    - gender: A string column showing the gender of the user. #marketing
    - email: A string column showing the email of the user. #marketing
    - custom_logs: A dictionary column keeping any unexpected data if emergency.
    - game_characters: The relationshiop columns showing the type of character of user. # multiplecharacter
    - sender: A relationship column showing the sender payload if the user is a part of sender a friendship.
    - receiver: A relationship column showing the receiver payload if the user is a part of receiver on a friendship.
    - point: The relationship columns showing all the points of the user.
    - activity: A relationship columns keeping track on the user activity, like daily login.
    - social_media: A relationship column showing which social media are connected by user.
    - access_token: A string column representing the access token of the user. (PENDING)
    """
    # REVIEW: consider if these are ok and can be added at the moment?
    # gonCoin = relationship("CoinGonModel", back_populates="user")
    # usdtCoin = relationship("CoinUsdtModel", back_populates="user")
    # usdcCoin = relationship("CoinUsdcModel", back_populates="user")
    # tonCoin = relationship("CoinTonModel", back_populates="user")
```

### Point Model

```py
"""
Represents a point entity and defines the structure of the "point" table in the database
Fields:
- id: An integer column representing the primary key of the "point" table in the database.
- amount: An integer column representing the total point thet the user has.
- owner_id: An integer column representing who is the owner of these points.
- extra_profit_per_hour: An integer column showing that the extra points the user can get based on the level, affected by unlockings on enhancement (MINE)
- created_at: A DateTime column representing the time when the point was created.
- updated_at: A DateTime column representing the time when the point was last updated.
- owner: A relationship column showing the owner payload of these points.
"""
```

### Activity Model

```py
 """
    Represents an activity entity and defines the structures of the "activity" table in the database

    Fields:
    - id: An integer column representing the primary key of the "activity" table.
    - is_logged_in: An boolena column showing if the user is logged in right now.
    - login_streak: An integer column showing the day that user logged in continously.
    - total_logins: An integer column showing the total login time of the user, +1 for each login time # REVIEW how long does it count as a login?
    - last_action_time: A dateime column showing when did the user trigger the action, if no action more than 2 hrs >>> inactive or force logout
    - last_login_time: A dateime column showing when did the user login to the app
    - created_at: A datetime column showing the time when the user was created.
    - updated_at: A datetime column showing the time when the user was updated.
    - user: The relationship column the user of this activity refer to

    """
```

### Friend Model

```py

"""
 Represents a friend entity and defines the structure of the "friend" table in the database

 Fields:
 - id: An integer column representing the primary key of the "friend" table.
 - status: Enum column representing the friendship status.
 - sender_id: An integer column showing which sent the friend code to receiver.
 - receiver_id: An integer column showing which received the friend code from sender.
 - created_at: A datetime column showing the time when the friend was created.
 - updated_at: A datetime column showing the time when the friend was updated.
 - sender: A relationship column showing the sender payload on single friendship.
 - receiver: A relationship column showing the receiver payload on single friendship.
 """
```

### Social Media Model

```py
"""
Represents a friend entity and defines the structure of the "character" table in the database.

Fields:
- id: An integer column representing the primary key of the "character" table.
- first_name: A string column showing the first name of the character.
- last_name: A string column showing the last name  of the character.
- gender: An integer column showing the gender of the character.
- title: A string column showing the title on the character >>> diff character diff characterStats.
- created_at: A datetime column showing the time when the user was created.
- updated_at: A datetime column showing the time when the user was updated.
- user: The relationship column who owns this character.
- stats: The relationship column showing the detail properties of this character.
"""
```

### Game Character Model

```py
"""
   Represents a friend entity and defines the structure of the "character" table in the database.
   Fields:
   - id: An integer column representing the primary key of the "character" table.
   - first_name: A string column showing the first name of the character.
   - last_name: A string column showing the last name  of the character.
   - gender: An integer column showing the gender of the character.
   - title: A string column showing the title on the character >>> diff haracter diff characterStats.
   - created_at: A datetime column showing the time when the user was created.
   - updated_at: A datetime column showing the time when the user was updated.
   - user: The relationship column who owns this character.
   - stats: The relationship column showing the detail properties of this character.
   """
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
      "args": ["main:app", "--reload"],
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
