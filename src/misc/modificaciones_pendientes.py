import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union

# 'Union[float, np.ndarray]' nos permite indicar que una variable
# puede ser un solo número (float) O un array de NumPy (np.ndarray)

def test():
    """Prueba que el paquete se ha cargado correctamente."""
    print("El paquete ha sido cargado exitosamente!")

# Clase base de generador fotovoltaico
class GenPanFV:
    """
    Representa un Generador Fotovoltaico (GFV), incluyendo paneles e inversor.
    
    Permite calcular la potencia generada bajo ciertas condiciones de
    irradiancia y temperatura, aplicando el recorte del inversor.
    """
    def __init__(self, 
                 Ppico: float, 
                 N: int, 
                 kp: float, 
                 eta: float, 
                 Pinv: float, 
                 mu: float = 2.0, 
                 Gstd: float = 1000.0, 
                 Tr: float = 25.0):
        """
        Inicializa el modelo del Generador Fotovoltaico.

        Args:
            Ppico (float): Potencia pico del panel (Wp).
            N (int): Número de paneles.
            kp (float): Coeficiente de T° de potencia (%/°C), ej: -0.0045.
            eta (float): Eficiencia del sistema (inversor, cables, etc.), ej: 0.95.
            Pinv (float): Potencia nominal del inversor (kW).
            mu (float): Parámetro del modelo (sin uso actual en tu código).
            Gstd (float): Irradiancia estándar (W/m²).
            Tr (float): Temperatura de referencia de celda (°C).
        """
        self.Ppico = Ppico
        self.kp = kp
        self.N = N
        self.eta = eta
        
        # Almacenamos Pinv en kW, que es como se usará.
        self.Pinv_kW = Pinv  
        
        self.mu = mu
        self.Gstd = Gstd
        self.Tr = Tr
        
        # Atributo para guardar la última potencia calculada (opcional)
        self.potencia_calculada = None

    def calcular_potencia(self, G: Union[float, np.ndarray], T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calcula la potencia generada (en kW) para una irradiancia G (W/m²)
        y una temperatura ambiente T (°C).
        
        Este método funciona tanto para valores individuales como para arrays de NumPy.
        
        Aplica el "clipping" (recorte) basado en la potencia del inversor (Pinv).
        """
        
        # 1. Calcular la Temperatura de la Celda (Tc)
        # Vectorizado: funciona para float y para np.ndarray
        Tc = T + 0.031 * G
        
        # 2. Calcular la potencia DC generada por los paneles (en W)
        # P_dc = self.N * (G / self.Gstd) * self.Ppico * (1 + self.kp * (Tc - self.Tr))
        
        # 3. Calcular la potencia AC final (en kW)
        # Se multiplica por 'eta' (eficiencia) y se divide por 1000 (W a kW)
        P_kW = self.N * (G / self.Gstd) * self.Ppico * (1 + self.kp * (Tc - self.Tr)) * self.eta * 1e-3
        
        # 4. Aplicar el "Clipping" del Inversor
        # La potencia generada no puede ser mayor que la potencia del inversor.
        # np.minimum es una función vectorizada que compara elemento a elemento.
        P_final_kW = np.minimum(P_kW, self.Pinv_kW)
        
        # Guardamos el resultado (opcional, pero útil)
        self.potencia_calculada = P_final_kW
        
        return P_final_kW

    def pot_media(self, potencia_generada: np.ndarray) -> float:
        """
        Calcula la potencia media a partir de un array de potencias.
        
        Args:
            potencia_generada (np.ndarray): Array de potencias (ej: el 
                                          resultado de calcular_potencia).
        
        Returns:
            float: La potencia media.
        """
        if potencia_generada is None or len(potencia_generada) == 0:
            return 0.0
        return np.mean(potencia_generada)

    def energia_total(self, potencia_generada: np.ndarray, intervalo_min: int = 10) -> float:
        """
        Calcula la energía total (en kWh) generada, asumiendo un
        intervalo de tiempo constante entre mediciones.
        
        Args:
            potencia_generada (np.ndarray): Array de potencias (en kW).
            intervalo_min (int): Intervalo de tiempo entre cada medición 
                                 (en minutos). Por defecto 10 min.
        
        Returns:
            float: La energía total generada (en kWh).
        """
        if potencia_generada is None or len(potencia_generada) == 0:
            return 0.0
            
        # Convertir el intervalo de minutos a horas
        intervalo_hs = intervalo_min / 60.0
        
        # Energía (kWh) = Suma de Potencias (kW) * Intervalo de tiempo (h)
        # Esto es una integración simple (método de rectángulos)
        energia_kwh = np.sum(potencia_generada) * intervalo_hs
        
        return energia_kwh
