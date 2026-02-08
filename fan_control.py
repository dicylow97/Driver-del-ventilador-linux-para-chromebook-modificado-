import subprocess
import time

# CONFIGURACIÓN
INTERVALO = 5
VELOCIDAD_MIN_PWM = 100 
# Cuántas lecturas promediar (5 lecturas * 5 seg = promedio de los últimos 25 seg)
VENTANA_SUAVIZADO = 5 

historial_temps = []

def obtener_temperatura_real():
    try:
        for i in range(10):
            try:
                with open(f"/sys/class/thermal/thermal_zone{i}/type", "r") as f:
                    tipo = f.read().strip()
                if "pkg_temp" in tipo or "coretemp" in tipo:
                    with open(f"/sys/class/thermal/thermal_zone{i}/temp", "r") as f:
                        return int(f.read().strip()) / 1000.0
            except:
                continue
        return 50.0
    except:
        return 50.0

def establecer_velocidad(pwm_value):
    try:
        subprocess.run(["ectool", "fancontrolmanual", "1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ectool", "fanduty", str(pwm_value)], check=True, stdout=subprocess.DEVNULL)
    except:
        pass

def calcular_pwm_suave(temp_actual, v_actual):
    # 1. Mantener historial para suavizar saltos repentinos
    historial_temps.append(temp_actual)
    if len(historial_temps) > VENTANA_SUAVIZADO:
        historial_temps.pop(0)
    
    # Usamos el promedio para decidir
    temp_promedio = sum(historial_temps) / len(historial_temps)
    
    # 2. Definir nueva velocidad según promedio
    if temp_promedio > 72:
        nueva_v = 255
    elif temp_promedio > 62:
        nueva_v = 190
    elif temp_promedio > 52:
        nueva_v = 140
    elif temp_promedio > 42:
        nueva_v = 100
    else:
        nueva_v = 100 # Mantenemos el mínimo para evitar el on/off

    # 3. LATENCIA/HISTÉRESIS AGRESIVA
    # Si la nueva velocidad es menor a la actual, solo bajamos si la 
    # temperatura promedio ha bajado considerablemente (margen de 5 grados)
    if nueva_v < v_actual:
        margen = 5
        if temp_promedio > (42 + margen if nueva_v == 100 else 52 + margen):
            return v_actual # Se queda en la velocidad alta un rato más

    return nueva_v

print("Controlador Inteligente Estabilizado Activo...")

v_actual = 100 # Empezamos en el mínimo funcional

while True:
    t_instante = obtener_temperatura_real()
    v_nueva = calcular_pwm_suave(t_instante, v_actual)
    
    if v_nueva != v_actual:
        print(f"Cambio suave: Temp Instante: {t_instante}°C -> Nueva Velocidad: {v_nueva} PWM")
        v_actual = v_nueva
    
    establecer_velocidad(v_actual)
    time.sleep(INTERVALO)
