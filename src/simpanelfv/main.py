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
 ## Caracterísitcas de la App
st.write("""
# Esta aplicación contiene las siguientes características:
- Configuración Personalizada: El usuario puede ingresar manualmente las especificaciones técnicas y características operativas del sistema generador que desea simular.
- 	Configuración Predefinida: Se ofrece la opción de utilizar un perfil predefinido, basado en los parámetros técnicos del generador perteneciente a la UTN Facultad Regional Santa Fe.
### Interfaz gráfica
-	Módulo de Cálculo: Sección central de la herramienta donde el usuario configura los parámetros de entrada, como pueden ser la cantidad de módulos fotovoltaicos, parámetros de los característicos de los módulos, potencia nominal de los equipos y demás opciones y la ejecución las simulaciones del sistema.
-	Dashboard (Panel de Control): Apartado dedicado a la visualización de resultados. Presenta los datos de salida mediante gráficos, métricas y figuras de análisis dinámicas.

### Limitaciones
La aplicación basará su enfoque al analisis físico-energtico y la facilidad de su uso, por lo cual  se excluyen las siguentes funcionalidades del proyecto.

- Ánalisis Economico: No realiza cálculos de viabilidad financiera, retorno de la inversión, costos de instalación o amortización, ya que  depended de variables externas (tarifas eléctricas, costos, impuestos) que son volátiles y escapan al alcance de este simulador.

- Dimensionamiento Automático: Simpanelfv es una herramienta de simulación y validación, no de diseño o dimensionamiento automático. La aplicación no sugiere una configuración óptima de paneles basada en un perfil de consumo.

- Análisis de Sombras y "Balance of System" (BOS): La simulación no contempla pérdidas de rendimiento ocasionadas por sombreado de objetos externos. Asimismo, el cálculo se centra en el rendimiento ideal del panel basado en la irradiancia y los datos del fabricante, sin simular las pérdidas específicas de componentes eléctricos del BOS.
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
     Miembros y Contactos:
- Francisco Moine: fmoine@frsf.utn.edu.ar
- Gonzalo Morel: gmorel@frsf.utn.edu.ar
- Leonel Oldrini: loldrini@frsf.ut.edu.ar
    
    Licencia MIT
    Repositorio Github Privado, por ahora
 
             """)
