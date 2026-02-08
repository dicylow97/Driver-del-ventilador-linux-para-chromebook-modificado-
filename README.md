# 🐧 Chromebook Fan Control for Linux

Este proyecto permite tomar el control inteligente del ventilador en Chromebooks con distribuciones de Linux (especialmente Fedora), evitando que el hardware lo apague automáticamente. Incluye un script en Python con lógica de suavizado (histéresis) y un instalador automático.

## 🚀 Características
* **Control Automático:** Ajusta la velocidad según la temperatura real del CPU.
* **Histéresis y Suavizado:** Evita que el ventilador acelere y frene constantemente por picos breves de calor.
* **Modo Servicio:** Se inicia automáticamente al encender la computadora mediante `systemd`.
* **Escala PWM:** Utiliza valores de 0 a 255 para una precisión total en el hardware del Chromebook.

## 📦 Contenido del Repositorio
* `ectool`: Binario encargado de la comunicación con el Embedded Controller (EC).
* `fan_control.py`: Script principal en Python que gestiona la lógica térmica.
* `chromebook-fan.service`: Configuración para el sistema de servicios de Linux.
* `instalar.sh`: Script de instalación automatizada.

## 🛠️ Instalación

1. **Clona o descarga este repositorio** en tu Chromebook.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Dale permisos de ejecución al instalador:
   ```bash
   chmod +x instalar.sh
