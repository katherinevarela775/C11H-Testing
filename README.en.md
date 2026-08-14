# Indestructible Chat — C11H Testing

Real-time chat application built with **TCP sockets** in Python (client-server architecture), accompanied by a professional-grade automated testing suite using **pytest**.

This repository demonstrates testing best practices: unit tests with mocks, integration tests with real sockets, test-driven development (TDD), and code coverage measurement with `pytest-cov`.

## Repository

- Repository URL: <https://github.com/katherinevarela775/C11H-Testing.git>

## Project structure

```
├── server.py               # Chat server (ChatServer) with multi-user support
├── client.py               # Chat client (ChatClient) with connection retries
├── practica.py             # pytest practice exercises (fixtures, parametrize, mocking)
├── tests/
│   ├── test_unit.py        # Unit tests with mocks (DummySocket) and fixtures
│   ├── test_integration.py # Integration tests with real sockets
│   └── test_tdd.py         # Tests following the Red-Green-Refactor cycle (TDD)
├── run_tests.bat           # Script that runs the suite and exports the coverage report
├── requirements.txt        # Project dependencies
├── Informe.md              # Detailed testing report (Spanish)
└── resultados_cobertura.txt # Raw coverage report
```

## Features

- **Multi-user server**: handles several clients simultaneously using threads.
- **Client commands**: `/exit`, `/help`, `/users`.
- **UTF-8 support**: messages with emojis and special characters.
- **Anonymous users**: if no name is entered, an automatic one is assigned.
- **Resilient client**: retries the connection up to 5 times if the server is unavailable.
- **Disconnection handling**: the server detects unexpected network drops and notifies other users.

## Prerequisites

- **Python 3.9+**
- **pip** (package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/katherinevarela775/C11H-Testing.git
   cd C11H-Testing
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the server

```bash
python server.py
```

You will see the message: `Servidor iniciado en 127.0.0.1:5000`. Press `Ctrl+C` to shut it down.

### 2. Start clients

Open another terminal (one per user) and run:

```bash
python client.py
```

The client will ask for a username and connect to the server. Available commands inside the chat:

| Command  | Description                        |
|----------|------------------------------------|
| `/exit`  | Leave the chat                     |
| `/help`  | Show the list of commands          |
| `/users` | See connected users                |

> **Note**: the client uses `127.0.0.1:5000` by default. To connect from another machine, change the host/port when instantiating `ChatClient(host, port)`.

## Running the tests

### Option A: Manually

```bash
python -m pytest tests/ -v --cov=. --cov-report=term
```

### Option B: Automated script (Windows)

```bash
run_tests.bat
```

This script runs the suite, measures coverage and saves the result into `resultados_cobertura.txt`, then prints it to the screen.

### Expected results

The suite covers positive, negative and exception cases with **86% total coverage**, exceeding the 80% quality standard.

## Test types

| Type         | File                        | Description                                                       |
|--------------|-----------------------------|-------------------------------------------------------------------|
| Unit         | `tests/test_unit.py`        | Isolated logic using `DummySocket`, fixtures, `capsys` and `parametrize` |
| Integration  | `tests/test_integration.py` | Real clients and servers over the local network (payload stress test, disconnections) |
| TDD          | `tests/test_tdd.py`         | Red-Green-Refactor cycle on the empty-message validation          |

## Technologies

- **Python** — sockets, threading, datetime
- **pytest** — testing framework
- **pytest-cov** — code coverage measurement
- **unittest.mock** — mocking to isolate network dependencies

## Versión en español

Para la versión en español de este documento, consulta [README.md](README.md).
