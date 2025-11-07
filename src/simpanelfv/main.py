import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lib import fcn_base as base

base.test()

gen_facultad = base.GenPanFV(240, 12, -4.4e-3, 0.97, 2.5, 2)

pot_punt = gen_facultad.pot_modelo_GFV(750, 25)
print(pot_punt)

datos = pd.read_excel("extra/Datos_climatologicos_Santa_Fe_2019.xlsx", index_col=0)
print(datos)
lista_G = datos['Irradiancia (W/m²)']
lista_T = datos['Temperatura (°C)']
# Irradiancia (W/m²)  Temperatura (°C)

pot_rang = gen_facultad.pot_generada_rango(lista_G, lista_T)

print(pot_rang)

plt.plot(pot_rang)
plt.show()