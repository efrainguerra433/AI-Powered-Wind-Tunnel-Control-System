from maix import camera, display, image, nn, app, pinmap, time, pwm
from controller import PIDController
from perception import VisionSystem

# Configuración de Hardware (PWM)
frecuencia = 1000
duty_base = 30
pwm_id = 7
pinmap.set_pin_function("A19", "PWM7")
out = pwm.PWM(pwm_id, freq=frecuencia, duty=duty_base, enable=True)

# Inicialización de IA y Percepción
model_path = "/model-163206.maixcam/model_163206.mud"
detector = nn.YOLOv5(model=model_path)
vision = VisionSystem(real_width=5.5, focal_length=365.4545, base_height=1.04)

# Inicialización de Cámara y Pantalla
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()


altura_objetivo = 0.75  #En cm
pid = PIDController(kp=500, ki=20, kd=5, setpoint=altura_objetivo, output_limits=(-30, 70))

tiempo_inicial = time.ticks_ms() / 1000.0

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
    
    if objs:
        obj = objs[0] 
        
     
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
  
        altura_m, dist_cm = vision.get_height(obj.w)
        
        # Lógica de Control
        output = pid.compute(altura_m)
        current_duty = duty_base + output
        out.duty(current_duty)
        
        # Telemetría
        tiempo_actual = (time.ticks_ms() / 1000.0) - tiempo_inicial
        print(f"{tiempo_actual:.3f}s - Duty: {current_duty:.2f}% - Altura: {altura_m:.3f}m")
        
        # Mostrar info en imagen
        img.draw_string(obj.x, obj.y - 15, f"H: {altura_m:.2f}m", color=image.COLOR_BLUE)

    dis.show(img)

# Apagar motor al salir
out.duty(0)