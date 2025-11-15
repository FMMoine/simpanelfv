import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def lib_test():
    print("The package has been succesfully loaded!")

# Clase base de generador fotovoltaico fundamental
class GenPanFV:
    """
    # Clase Generador fotovoltaico elemental
    """

    def __init__(self, Ppico, N, kp, eta, Pinv, mu=2, Gstd = 1000, Tr=25):
        self.Ppico = Ppico
        self.kp = kp
        self.N = N
        self.eta = eta
        self.Pinv = Pinv
        self.mu = mu
        self.Gstd = Gstd
        self.Tr = Tr
        self.listaP = np.array([0])

    def pot_modelo_GFV(self, G, T):
        """
        Devuelve la potencia generada por un GFV con los datos indicados, cuando la irradiancia es G y la temperatura ambiente es T.
        """
        Tc = T + 0.031 * G
        P = self.N * (G / self.Gstd) * self.Ppico * (1 + self.kp * (Tc - self.Tr)) * self.eta * 1e-3

        return P

    def pot_generada_rango(self, lista_G, lista_T):
        """
        Simil anterior, pero recibe en lista_G una lista (o vector) con
        cualquier cantidad de valores de irradiancia, y en lista_T una
        con igual cantidad de registros de temperatura ambiente.
        Devuelve otra lista (o contenedor) con las potencias generadas para
        cada par de valores de irradiancia y temperatura.

        """

        Tc = lista_T + 0.031 * lista_G
        P = self.N * (lista_G / self.Gstd) * self.Ppico * (1 + self.kp * (Tc - self.Tr)) * self.eta * 1e-3

        self.listaP = P


    # Functiones que manipulan la informacion obtenida a traves de los datos ingresados (ie lista de potencia generada)
    def pot_media(self):
        """
        Recibe los mismos argumentos que la función anterior, y devuelve
        la potencia que resulta de promediar todas las calculadas con
        cada par de valores de irradiancia y temperatura ambiente.
        """
        return self.listaP.mean()

    def energia(self):
        """
        # Recibe los mismos argumentos que la función anterior, y devuelve
        # la energía generada por el GFV (en kWh), asumiendo que el intervalo
        # de tiempo transcurrido entre 2 mediciones de irradiancia (o de temp.)
        # es de 10 minutos.
        """
        nrg = self.listaP * (1/6)
        return nrg.sum()

    def factor_de_utilizacion(self):
        """
        # Recibe los mismos argumentos que la función anterior, y devuelve
        # el factor de utilización del GFV, definido como la energía
        # generada en un período dividido por la energía que se hubiera
        # generado si el GFV hubiera operado a potencia pico durante
        # todo el período.
        """
        energia_generada = self.energia()
        energia_pico = self.Ppico * self.N * (len(self.listaP) * (1/6))

        fdu = energia_generada / energia_pico
        return fdu
# gen1 = GenPanFV(240, 12, -4.4e-3, 0.97, 2.5, 2)