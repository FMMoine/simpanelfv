import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

st.write("""
# Datos de entrada y configuración de la información de salida
         """)

arch_data = st.file_uploader(label='Carga Excel', accept_multiple_files=False)

if arch_data is not None:
   try:
            tabla = pd.read_excel(arch_data)
            mapa_nombres = {
                     'Irradiancia (W/m²)': 'G',
                     'Irradiancia (W/m2)': 'G',
                     'Irradiancia': 'G',
                     'Temperatura (°C)': 'T',
                     'Temperatura (C)': 'T',
                     'Temperatura': 'T'
            }
            tabla = tabla.rename(columns=mapa_nombres)
            if 'G' in tabla.columns and 'T' in tabla.columns:
                     st.success("Archivo validado correctamente.")
                     st.session_state['df_clima']=tabla
                     st.session_state ['datos_cargados']=True
                     st.write("Vista previa de los datos:")
                     st.dataframe(tabla)
                     st.info("Datos procesados. Podés pasar a la sección 'Cálculo' para simular.")
            else:
                     st.error("El archivo no tiene el formato correcto.")
                     st.warning("El excel debe tener una columna llamada **'G'** (Irradiancia) y otra **'T'** (Temperatura)")
                     st.write("Columnas encontradas:",tabla.columns.tolist())
   except Exception as e:
            st.error(f"Error al leer el archivo:{e}")
                           
else:
         st.info("Esperando carga de archivo")
