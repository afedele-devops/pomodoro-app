#!/bin/bash

echo "🔍 Comprobando entorno virtual..."

# Verificar si python3-venv está instalado
if ! dpkg -s python3-venv &> /dev/null; then
    echo "⚠️ El paquete 'python3-venv' no está instalado."
    echo "👉 Instálalo con: sudo apt update && sudo apt install python3-venv"
    exit 1
fi

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "⚙️ Creando entorno virtual..."
    python3 -m venv venv
fi

# Detectar si ya estamos dentro de un venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📂 Activando entorno virtual..."
    source venv/bin/activate
else
    echo "✅ Ya estás dentro de un entorno virtual."
fi

echo "🔍 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Dependencias listas."
echo "🚀 Iniciando Pomodoro Timer..."
python3 pomodoro.py

