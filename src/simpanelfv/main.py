import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

lib_test()

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

print(gen_facultad.pot_media(), gen_facultad.energia())

pages = {
    "Información General": [
        st.Page("pages/01_inicio.py", title="Inicio"),
        st.Page("pages/04_marteor.py", title="Marco Teórico"),
        st.Page("pages/05_about.py", title="Learn about us"),
    ],

    "Configuración": [
        st.Page("pages/02a_configuracion.py", title="Generador Fotovoltaico"),
        st.Page("pages/02b_configuracion.py", title="Datos de Entrada y Salida"),
    ],

    "Cálculos": [
        st.Page("pages/03a_calculos.py", title="Modelado"),
        st.Page("pages/03b_calculos.py", title="Gráficos"),
        st.Page("pages/03c_calculos.py", title="Extras"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
