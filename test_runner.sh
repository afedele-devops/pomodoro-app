#!/bin/bash

echo "🧪 Iniciando pruebas del Pomodoro Timer..."

# 1. Validar dependencias
REQUIREMENTS_FILE="requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "🔍 Verificando dependencias en $REQUIREMENTS_FILE..."
    pip install --upgrade pip
    pip install -r $REQUIREMENTS_FILE
else
    echo "⚠️ No se encontró $REQUIREMENTS_FILE. Creando uno básico..."
    cat <<EOL > requirements.txt
fastapi
uvicorn
pytest
pytest-playwright
EOL
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 2. Instalar navegadores de Playwright si no están presentes
if ! command -v playwright &> /dev/null; then
    echo "⚠️ Playwright no está instalado. Instalando..."
    pip install playwright
fi

echo "📦 Instalando navegadores de Playwright..."
playwright install

# 3. Levantar el servidor en segundo plano
python pomodoro.py &
SERVER_PID=$!

# 4. Esperar unos segundos para que el servidor arranque
sleep 5

# 5. Ejecutar pytest
pytest -v test_pomodoro.py
TEST_RESULT=$?

# 6. Finalizar el servidor
kill $SERVER_PID

# 7. Mostrar resultado
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ Todas las pruebas pasaron correctamente."
else
    echo "❌ Algunas pruebas fallaron."
fi

exit $TEST_RESULT
