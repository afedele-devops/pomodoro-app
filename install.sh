#!/bin/bash

echo "🔧 Instalación del entorno Pomodoro Timer"

# 1. Verificar si python3-venv está instalado
if ! dpkg -s python3-venv &> /dev/null; then
    echo "⚠️ El paquete 'python3-venv' no está instalado."
    echo "👉 Instalando con sudo apt..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# 2. Eliminar venv previo si existe
if [ -d "venv" ]; then
    echo "🗑️ Eliminando entorno virtual anterior..."
    rm -rf venv
fi

# 3. Crear nuevo entorno virtual
echo "⚙️ Creando entorno virtual..."
python3 -m venv venv

# 4. Activar entorno virtual
echo "📂 Activando entorno virtual..."
source venv/bin/activate

# 5. Instalar dependencias
if [ -f requirements.txt ]; then
    echo "📦 Instalando dependencias desde requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "⚠️ No se encontró requirements.txt, omitiendo instalación de dependencias."
fi

echo "✅ Instalación completa."
echo "👉 Ahora puedes ejecutar: ./start.sh"
