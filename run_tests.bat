@echo off # oculta visual. del comando en la consola
echo Ejecutando pruebas y generando reporte crudo...
python -m pytest tests/ -v --cov=. --cov-report=term > resultados_cobertura.txt
echo Pruebas finalizadas. Resultados guardados en resultados_cobertura.txt
type resultados_cobertura.txt