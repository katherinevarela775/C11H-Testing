Informe de Testing - Chat Indestructible
1. Resumen de Herramientas y Entorno
Para este challenge, se configuró un entorno de pruebas automatizado de nivel profesional utilizando:

pytest: Framework principal de pruebas unitarias e integración.

pytest-cov: Herramienta para la medición estricta de la cobertura de código (Code Coverage).

Patrones avanzados de Pytest: Implementación de Fixtures, fábricas con yield (para gestión automática de Setup/Teardown), parametrización de pruebas (@pytest.mark.parametrize), captura de consola (capsys), control de excepciones (pytest.raises) y marcadores globales (pytestmark).

Automatización: Script de lotes (run_tests.bat) para la ejecución unificada de la suite y exportación automática de reportes de cobertura en la terminal.

2. Decisiones de Arquitectura e Insights (Refactorización)
Durante el desarrollo, se aplicaron principios de Clean Code y diseño modular para aislar responsabilidades:

Transición a POO: La lógica del servidor y el cliente se encapsuló en clases (ChatServer y ChatClient), eliminando variables globales y permitiendo la ejecución concurrente e independiente de múltiples instancias en los tests.

Inyección de Dependencias (Fixtures): Se utilizaron fixtures de Pytest para suministrar servidores y clientes limpios a las pruebas, automatizando la apertura y cierre de recursos (puertos e hilos) sin repetir código (Principio DRY).

Mocking (Sockets Falsos): Se desarrolló la clase DummySocket para aislar la lógica de red de las pruebas unitarias, permitiendo simular envíos, recepciones, tiempos de espera y desconexiones remotas sin consumir recursos físicos reales.

Control de Hilos y Timeouts: Se integraron banderas booleanas (self.running) y temporizadores en los sockets para evitar bloqueos infinitos y procesos zombies durante la apertura y cierre de servicios.

3. Registro de Pruebas Realizadas
A. Pruebas Unitarias y Mocks (test_unit.py)
test_formatear_mensaje_positivo (Happy Path): Verifica que el servidor empaquete correctamente el texto con su respectiva marca de tiempo y estructura de corchetes.

test_formatear_mensaje_negativo_vacio: Utiliza pytest.raises para asegurar que el sistema lance un ValueError intencional ante la entrada de espacios en blanco.

test_conectar_negativo_ip_invalida: Comprueba que el cliente maneja excepciones de red críticas (apuntando a una IP imposible) retornando False en lugar de colapsar la aplicación.

test_cliente_enviar_mensajes_normal y test_cliente_enviar_mensajes_exit: Emplean DummySocket y funciones de input simuladas para validar el flujo de salida de datos y el auto-apagado con el comando /exit.

test_cliente_recibir_mensajes_positivo: Utiliza el fixture capsys de Pytest para capturar la salida estándar (stdout), verificando que los mensajes entrantes se imprimen correctamente en consola antes de detectar la caída del servidor.

test_remover_cliente_existente_positivo / inexistente_negativo: Validan la gestión segura del diccionario de memoria del servidor al eliminar clientes activos o procesar llaves inexistentes sin generar excepciones nativas.

test_cliente_desconectar_positivo: Comprueba la correcta actualización de los estados internos de ejecución al cerrar las conexiones.

test_procesar_comandos_rutas_completas: Aplica @pytest.mark.parametrize para evaluar de forma masiva y limpia las 4 rutas posibles del servidor (/help, /users, /exit y mensajes normales).

B. Desarrollo Guiado por Pruebas - TDD (test_tdd.py)
Funcionalidad implementada: Mecanismo de validación estricta para rechazar mensajes vacíos o compuestos únicamente por espacios.

Ciclo aplicado:

Red: Escritura inicial de pruebas exigiendo el rechazo de strings vacíos.

Green: Desarrollo de la lógica condicional en el servidor para retornar False.

Refactor: Optimización mediante expresiones booleanas eficientes integradas al flujo operativo.

C. Pruebas de Integración y Estrés de Red (test_integration.py)
test_integracion_envio_y_recepcion: Simula la conexión de dos clientes en un entorno real. Utiliza @pytest.mark.parametrize para realizar un Payload Stress Test, inyectando texto normal, emojis y caracteres especiales para garantizar la integridad de la codificación utf-8.

test_desconexion_inesperada_cliente: Fuerza el cierre abrupto del socket del Cliente A (simulando un corte de red sin usar /exit). Valida que el servidor notifica al Cliente B y elimina limpiamente al usuario de su registro interno.

test_integracion_simultanea_y_orden: Evalúa una red con 3 clientes concurrentes. Implementa rutinas de limpieza de buffers por temporizador y comprueba que el servidor procesa mensajes enviados simultáneamente sin pérdidas ni alteraciones en el orden de llegada.

test_desconexion_masiva_y_durante_transmision: Simula un escenario de fallo crítico donde múltiples clientes se desconectan de manera simultánea justo durante la transmisión de datos. Comprueba la resiliencia del servidor, la purga de memoria y la operatividad continua de los clientes sobrevivientes.

4. Resultados de Cobertura (Code Coverage)
La ejecución integral de la suite de pruebas mediante el script automatizado arrojó una cobertura total del 86% del proyecto, superando ampliamente el estándar de calidad del 80% requerido y garantizando la robustez ante casos positivos, negativos y excepciones de red.