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

inicio, config, calc, marteor, extras = st.tabs(["Inicio", "Configuración", "Cálculos y Resultados", "Marco Teórico", "About"])

with inicio:
    st.write("""
        # SimPanelFV
        Simulador de generación de equipo de paneles fotovoltaicos
        """)
    st.latex(r"""
        \frac{a}{b}
    """)

with config:
    arch_data = st.file_uploader(label='Carga Excel', accept_multiple_files=False)

    if arch_data is not None:
        tabla = pd.read_excel(arch_data)
        st.dataframe(tabla)    

with calc:
    ejemplo_tabla = pd.DataFrame(data={
        "Valores": [1, 2, 3, 4, 5, 6],
        "Categorias": ["A", "B", "C", "D", "E", "F"]
    })

    st.dataframe(ejemplo_tabla)
    fig = px.pie(ejemplo_tabla, names='Categorias', values='Valores')
    st.plotly_chart(fig)

with extras:
    st.write("""
     Miemros y Contacto:
    - Francisco Moine 
    - Gonzalo Morel 
    - Leonel Oldrini
    
    Licencia MIT
    Repositorio Github Privado, por ahora
 
             """)
