import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GenPanFV:
    """
    Clase que modela un Generador Fotovoltaico y su inversor asociado.
    Almacena los parámetros fijos y calcula la potencia y energía generada.
    """

    def __init__(self, Ppico, N, kp, eta, Pinv, mu=2.0, Gstd=1000.0, Tr=25.0):
        self.Ppico = Ppico  # Potencia pico de un módulo (W)
        self.kp = kp        # Coeficiente de temperatura (1/°C)
        self.N = N          # Número de módulos
        self.eta = eta      # Rendimiento (inversor, cableado, etc.)
        self.Pinv = Pinv    # Potencia nominal del inversor (kW)
        self.mu = mu        # Umbral porcentual mínimo del inversor (%)
        self.Gstd = Gstd    # Irradiancia estándar (W/m²)
        self.Tr = Tr        # Temperatura de referencia (°C)
        
        # Potencia mínima de arranque del inversor (en kW)
        self.P_min = (self.mu / 100) * self.Pinv 
        
        # Array para almacenar de forma interna una serie de potencias calculada
        self.__listaP = None

    @property
    def listaP(self):
        return self.__listaP

    def _calcular_potencia_bruta(self, G, T):
        """
        Método privado para calcular la potencia teórica (bruta) del GFV
        antes de aplicar los límites del inversor.
        G y T pueden ser valores únicos o arrays de numpy.
        """
        # 1. Calcular Temperatura de la Celda (Tc)
        Tc = T + 0.031 * G
        
        # 2. Calcular Potencia Bruta (P_bruta) en kW
        P_bruta = self.N * (G / self.Gstd) * self.Ppico * (1 + self.kp * (Tc - self.Tr)) * self.eta * 1e-3
        return P_bruta

    def pot_modelo_GFV(self, G, T):
        """
        Devuelve la potencia generada (en kW) por el GFV, aplicando
        los límites del inversor (P_min y Pinv) para una única
        irradiancia G (W/m²) y temperatura T (°C).
        """
        # Calcula la potencia bruta (teórica)
        P_bruta = self._calcular_potencia_bruta(G, T)
        
        # Aplicar límites del inversor
        if P_bruta < self.P_min:
            return 0.0
        elif P_bruta > self.Pinv:
            return self.Pinv
        else:
            return P_bruta

    def pot_generada_rango(self, lista_G, lista_T):
        """
        Recibe listas (o arrays) de irradiancia y temperatura y
        devuelve un array de numpy con las potencias generadas (en kW),
        aplicando los límites del inversor.
        """
        # Asegurarse de que sean arrays de numpy para operación vectorial
        lista_G_np = np.array(lista_G)
        lista_T_np = np.array(lista_T)
        
        # Calcular la potencia bruta (teórica) para todo el rango
        P_bruta_array = self._calcular_potencia_bruta(lista_G_np, lista_T_np)
        
        # Aplicar límites del inversor de forma vectorial
        # 1. Si P_bruta es menor que P_min, la potencia es 0.
        P_limitada = np.where(P_bruta_array < self.P_min, 0.0, P_bruta_array)
        
        # 2. Si la potencia supera al inversor, se clava en Pinv.
        P_final = np.where(P_limitada > self.Pinv, self.Pinv, P_limitada)
        
        # Guardar el resultado en la instancia y devolverlo
        self.__listaP = P_final.tolist()
        return self.__listaP

    def pot_media(self):
        """
        Devuelve la potencia media (en kW) de la última simulación
        almacenada en self.listaP.
        """
        if self.__listaP is None:
            return 0.0
        return np.mean(self.__listaP)

    def energia(self, PotExt):
        """
        Devuelve la energía total generada (en kWh) de la última simulación,
        asumiendo intervalos de 10 minutos (1/6 de hora).
        """
        
        # Intervalo de tiempo en horas (10 min = 1/6 h)
        intervalo_h = 10 / 60
        
        # Energía = Suma de (Potencia_i * intervalo_h)
        nrg = np.sum(PotExt) * intervalo_h

        return nrg

    def factor_de_utilizacion(self):
        """
        Devuelve el factor de utilización (adimensional).
        Se calcula como la energía generada dividida por la energía
        que el INVERSOR podría haber entregado a potencia nominal.
        """
        energia_generada = self.energia()
        
        if self.__listaP is None:
            return 0.0
            
        # Intervalo de tiempo en horas (10 min = 1/6 h)
        intervalo_h = 10 / 60
        
        # Energía nominal = Potencia del INVERSOR * tiempo total
        tiempo_total_h = len(self.__listaP) * intervalo_h
        energia_nominal_inversor = self.Pinv * tiempo_total_h

        if energia_nominal_inversor == 0:
            return 0.0
            
        fdu = energia_generada / energia_nominal_inversor
        return fdu

    def max_pot(self, PotExt):
        """
        Devuelve una tupla (índice, valor) de la potencia máxima
        identificada en la última simulación.
        """
            
        max_P_val = np.max(PotExt)
        max_P_idx = np.argmax(PotExt)
        return (max_P_val, max_P_idx)

    def graficar_pot(self):
        """
        Genera y devuelve una figura de Matplotlib con la variación
        temporal de la potencia de la última simulación.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(self.__listaP) > 0:
            n_puntos = len(self.__listaP)
            # El tiempo total es n_puntos * 10 minutos. Lo pasamos a horas.
            tiempo_horas = np.arange(0, n_puntos * 10 / 60, 10 / 60)
            
            ax.plot(tiempo_horas, self.__listaP, label='Potencia Generada')
            
            # Líneas de referencia
            ax.axhline(y=self.Pinv, color='r', linestyle='--', label=f'Pot. Nominal Inversor ({self.Pinv} kW)')
            ax.axhline(y=self.P_min, color='orange', linestyle='--', label=f'Pot. Mínima ({self.P_min:.2f} kW)')
            
            ax.set_xlabel("Tiempo (horas)")
            ax.set_ylabel("Potencia Generada (kW)")
            ax.set_title("Variación Temporal de la Potencia del GFV")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "No hay datos para graficar. Ejecute 'pot_generada_rango' primero.", 
                    horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            
        return fig
    
def lib_test():
    """
    Función de testeo para verificar que el módulo se importa correctamente.
    """

    gen_facultad = GenPanFV(240, 12, -4.4e-3, 0.97, 2.5, 2)

    pot_punt = gen_facultad.pot_modelo_GFV(750, 25)
    print(pot_punt)

    datos = pd.read_excel("data/Datos_climatologicos_Santa_Fe_2019.xlsx", index_col=0)
    # print(datos)
    lista_G = datos['Irradiancia (W/m²)']
    lista_T = datos['Temperatura (°C)']
    # Irradiancia (W/m²)  Temperatura (°C)

    gen_facultad.pot_generada_rango(lista_G,lista_T)
    pot_rang = gen_facultad.listaP

    print("Rango de Potencias")
    print(pot_rang, type(pot_rang))

    plt.plot(pot_rang)
    plt.show()

    print(gen_facultad.pot_media(), gen_facultad.energia(gen_facultad.listaP))

    print("El módulo fcn_base.py se ha cargado correctamente.")