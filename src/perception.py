class VisionSystem:
    def __init__(self, real_width=5.5, focal_length=365.45, base_height=1.04):
        self.W_real = real_width
        self.f = focal_length
        self.base_height = base_height

    def get_height(self, pixel_width):
        # Calcular distancia de la cámara al objeto en cm
        distance_cm = (self.W_real * self.f) / pixel_width
        
        # Convertir a altura relativa al suelo/base en metros
        altura_actual = self.base_height - (distance_cm / 100)
        return altura_actual, distance_cm