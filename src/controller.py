from maix import time

class PIDController:
    def __init__(self, kp, ki, kd, setpoint, output_limits=(0, 100)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.output_limits = output_limits
      
        self.last_error = 0
        self.integral = 0
        self.last_time = time.ticks_ms() / 1000.0
        
    def compute(self, process_variable):
        # Calcular tiempo transcurrido
        current_time = time.ticks_ms() / 1000.0
        dt = current_time - self.last_time

        if dt <= 0:
            return 0
            
        # Calcular error
        error = self.setpoint - process_variable
        

        p_term = self.kp * error
        
        # Término integral
        self.integral += error * dt
        i_term = self.ki * self.integral
        
        # Término derivativo
        derivative = (error - self.last_error) / dt
        d_term = self.kd * derivative
        
        #salida total
        output = p_term + i_term + d_term
        
        # Limitar salida (Anti-windup básico)
        output = max(self.output_limits[0], min(self.output_limits[1], output))
        
        # Actualizar estados
        self.last_error = error
        self.last_time = current_time
        
        return output
