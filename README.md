# Chat Indestructible — C11H Testing

Aplicación de chat en tiempo real construida con **sockets TCP** de Python (arquitectura cliente-servidor), acompañada de una suite de pruebas automatizada de nivel profesional con **pytest**.

Este repositorio demuestra buenas prácticas de testing: pruebas unitarias con mocks, pruebas de integración con sockets reales, desarrollo guiado por pruebas (TDD) y medición de cobertura de código con `pytest-cov`.

## Repositorio

- URL del repositorio: <https://github.com/katherinevarela775/C11H-Testing.git>

## Estructura del proyecto

```
├── server.py               # Servidor de chat (ChatServer) con soporte multiusuario
├── client.py               # Cliente de chat (ChatClient) con reintentos de conexión
├── practica.py             # Ejercicios prácticos de pytest (fixtures, parametrize, mocking)
├── tests/
│   ├── test_unit.py        # Pruebas unitarias con mocks (DummySocket) y fixtures
│   ├── test_integration.py # Pruebas de integración con sockets reales
│   └── test_tdd.py         # Pruebas del ciclo Red-Green-Refactor (TDD)
├── run_tests.bat           # Script que ejecuta la suite y exporta el reporte de cobertura
├── requirements.txt        # Dependencias del proyecto
├── Informe.md              # Informe detallado de testing
└── resultados_cobertura.txt # Reporte crudo de cobertura
```

## Funcionalidades

- **Servidor multiusuario**: atiende varios clientes simultáneamente usando hilos (`threading`).
- **Comandos del cliente**: `/exit`, `/help`, `/users`.
- **Soporte UTF-8**: mensajes con emojis y caracteres especiales.
- **Usuarios anónimos**: si no se ingresa un nombre, se asigna uno automático.
- **Cliente resiliente**: reintenta la conexión hasta 5 veces si el servidor no está disponible.
- **Manejo de desconexiones**: el servidor detecta caídas de red inesperadas y notifica a los demás usuarios.

## Requisitos previos

- **Python 3.9+**
- **pip** (gestor de paquetes)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/katherinevarela775/C11H-Testing.git
   cd C11H-Testing
   ```

2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

### 1. Iniciar el servidor

```bash
python server.py
```

Verás el mensaje: `Servidor iniciado en 127.0.0.1:5000`. Presiona `Ctrl+C` para apagarlo.

### 2. Iniciar clientes

Abre otra terminal (una por cada usuario) y ejecuta:

```bash
python client.py
```

El cliente pedirá un nombre de usuario y se conectará al servidor. Comandos disponibles dentro del chat:

| Comando   | Descripción                          |
|-----------|--------------------------------------|
| `/exit`   | Salir del chat                       |
| `/help`   | Mostrar la lista de comandos         |
| `/users`  | Ver los usuarios conectados          |

> **Nota**: el cliente usa `127.0.0.1:5000` por defecto. Para conectar desde otra máquina, cambia el host/puerto al instanciar `ChatClient(host, port)`.

## Ejecutar las pruebas

### Opción A: Manual

```bash
python -m pytest tests/ -v --cov=. --cov-report=term
```

### Opción B: Script automático (Windows)

```bash
run_tests.bat
```

Este script ejecuta la suite, mide la cobertura y guarda el resultado en `resultados_cobertura.txt`, mostrándolo luego en pantalla.

### Resultados esperados

La suite cubre casos positivos, negativos y de excepción con una **cobertura total del 86%**, superando el estándar del 80%.

## Tipos de pruebas

| Tipo            | Archivo                  | Descripción                                                       |
|-----------------|--------------------------|-------------------------------------------------------------------|
| Unitarias       | `tests/test_unit.py`     | Lógica aislada usando `DummySocket`, fixtures, `capsys` y `parametrize` |
| Integración     | `tests/test_integration.py` | Clientes y servidores reales sobre la red local (payload stress test, desconexiones) |
| TDD             | `tests/test_tdd.py`      | Ciclo Red-Green-Refactor sobre la validación de mensajes vacíos   |

## Tecnologías

- **Python** — sockets, threading, datetime
- **pytest** — framework de pruebas
- **pytest-cov** — medición de cobertura de código
- **unittest.mock** — mocking para aislar dependencias de red

## English version

Para la versión en inglés de este documento, consulta [README.en.md](README.en.md).
