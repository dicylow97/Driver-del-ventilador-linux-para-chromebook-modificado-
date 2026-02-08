#!/bin/bash

# Colores para la terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
ROJO='\033[0;31m'
NC='\033[0m' 

echo -e "${AZUL}--- Iniciando Instalación Completa (Incluyendo ectool) ---${NC}"

# 1. Instalar el binario de ectool que tienes en la carpeta
if [ -f "./ectool" ]; then
    echo "Instalando binario ectool en /usr/local/sbin..."
    sudo cp ./ectool /usr/local/sbin/ectool
    sudo chmod +x /usr/local/sbin/ectool
    # Verificación de que funciona
    if /usr/local/sbin/ectool version &>/dev/null; then
        echo -e "${VERDE}[OK]${NC} ectool instalado y funcionando."
    else
        echo -e "${ROJO}[ADVERTENCIA]${NC} ectool instalado pero devolvió un error de ejecución."
    fi
else
    echo -e "${ROJO}Error: No se encontró el archivo 'ectool' en esta carpeta.${NC}"
    exit 1
fi

# 2. Instalar el script de Python
if [ -f "./fan_control.py" ]; then
    echo "Instalando script de control en /usr/local/bin..."
    sudo cp ./fan_control.py /usr/local/bin/fan_control.py
    sudo chmod +x /usr/local/bin/fan_control.py
    # Ajustar la ruta de ectool dentro del script de python por si acaso
    sudo sed -i 's|ectool|/usr/local/sbin/ectool|g' /usr/local/bin/fan_control.py
else
    echo -e "${ROJO}Error: No se encontró 'fan_control.py'.${NC}"
    exit 1
fi

# 3. Instalar el servicio de Systemd
if [ -f "./chromebook-fan.service" ]; then
    echo "Configurando servicio de sistema..."
    sudo cp ./chromebook-fan.service /etc/systemd/system/chromebook-fan.service
    
    # Recargar y activar
    sudo systemctl daemon-reload
    sudo systemctl enable chromebook-fan.service
    sudo systemctl restart chromebook-fan.service
    echo -e "${VERDE}[OK]${NC} Servicio activado y habilitado para el arranque."
else
    echo -e "${ROJO}Error: No se encontró 'chromebook-fan.service'.${NC}"
    exit 1
fi

echo -e "${VERDE}--------------------------------------------------${NC}"
echo -e "TODO LISTO. El ventilador ahora es automático."
echo -e "Estado actual: $(sudo systemctl is-active chromebook-fan.service)"
echo -e "${VERDE}--------------------------------------------------${NC}"
echo -e "Ahora queda reiniciar, Usa este comando: sudo reboot"
echo -e "${VERDE}--------------------------------------------------${NC}"

