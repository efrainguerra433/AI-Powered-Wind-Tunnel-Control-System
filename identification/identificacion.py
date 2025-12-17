from maix import camera, display, image, nn, app, pinmap, time, pwm

# --- CONFIGURACIÓN DE HARDWARE ---
RUTA_SEÑAL_EXCITACION = "/root/CTR2/numeros_3p.txt"
FRECUENCIA_PWM = 1000 
DUTY_OPERACION = 34  
PWM_ID = 7

pinmap.set_pin_function("A19", "PWM7")
out = pwm.PWM(PWM_ID, freq=FRECUENCIA_PWM, duty=50, enable=True)

# --- FASE INICIAL: Estabilización ---
print("Estabilizando sistema...")
time.sleep(10)
out.duty(DUTY_OPERACION)
current_duty = DUTY_OPERACION

# --- CONFIGURACIÓN DE VISIÓN (IA) ---
detector = nn.YOLOv5(model="/root/CTR2/model-163206.maixcam/model_163206.mud")
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()

W_REAL = 5.5  # cm
FOCAL_PIXELS = 365.45

def cargar_variaciones(ruta):
    try:
        with open(ruta, 'r') as f:
            return [float(linea.strip()) for linea in f if linea.strip()]
    except Exception as e:
        print(f"Error leyendo archivo de excitación: {e}")
        return []

# --- BUCLE DE CAPTURA DE DATOS ---
datos_excitacion = []
indice_actual = 0
tiempo_inicio_experimento = None

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
    
    # Percepción y Salida de datos para MATLAB
    if objs:
        obj = objs[0]
        # Calcular distancia y altura (104 cm es la altura total del túnel)
        distancia = (W_REAL * FOCAL_PIXELS) / obj.w
        altura_actual = 104 - distancia 
     
        print(f"{current_duty * 0.001} - {altura_actual}")
        
        # Visualización básica
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
    
    dis.show(img)
    
    # Lógica de Inyección de Señal (Variaciones aleatorias)
    tiempo_actual = time.time()
    
    if not datos_excitacion:
        datos_excitacion = cargar_variaciones(RUTA_SEÑAL_EXCITACION)
        if datos_excitacion:
            tiempo_inicio_experimento = tiempo_actual
    
    # Aplicar nueva variación cada 30 segundos 
    if datos_excitacion and tiempo_inicio_experimento:
        if tiempo_actual - tiempo_inicio_experimento >= 30:
            if indice_actual < len(datos_excitacion):
                valor_variacion = datos_excitacion[indice_actual]
                current_duty = DUTY_OPERACION + valor_variacion
                out.duty(current_duty)
                indice_actual += 1
            else:
                # Fin del experimento
                datos_excitacion = []
                indice_actual = 0
                tiempo_inicio_experimento = None

out.duty(0)
