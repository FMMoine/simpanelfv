import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

def_N = st.session_state.get('N', 10)
def_Ppico = st.session_state.get('Ppico', 330.0)
def_kp = st.session_state.get('kp', -0.0040)
def_Pinv = st.session_state.get('Pinv', 3.0)
def_eta = st.session_state.get('eta', 0.90)
def_mu = st.session_state.get('mu', 2.0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Datos del Panel (FV)")
    # Cantidad de paneles
    input_N = st.number_input("Número de módulos (N)", 
                              value=def_N, step=1, min_value=1)
    # Potencia pico
    input_Ppico = st.number_input("Potencia Pico del módulo (W)", 
                                  value=def_Ppico, step=10.0)
    # Coeficiente de temperatura
    input_kp = st.number_input("Coeficiente de Temp. (kp) [1/°C]", 
                               value=def_kp, step=0.0001, format="%.4f")
with col2:
    st.subheader("Datos del Inversor")
    # Potencia Inversor
    input_Pinv = st.number_input("Potencia Nominal Inversor (kW)", 
                                 value=def_Pinv, step=0.5)
    # Rendimiento
    input_eta = st.number_input("Rendimiento Global (eta) [0-1]", 
                                value=def_eta, step=0.01, max_value=1.0)
    # Umbral mínimo
    input_mu = st.number_input("Umbral mínimo de arranque (%)", 
                               value=def_mu, step=0.5)
st.divider()
# --- 3. BOTÓN DE GUARDADO ---
if st.button("Guardar Configuración", type="primary"):
    
    # Guardamos los valores que escribió el usuario
    st.session_state['N'] = input_N
    st.session_state['Ppico'] = input_Ppico
    st.session_state['kp'] = input_kp
    st.session_state['Pinv'] = input_Pinv
    st.session_state['eta'] = input_eta
    st.session_state['mu'] = input_mu
    
    st.session_state['config_guardada'] = True

    st.success("¡Configuración guardada correctamente!")
    st.info("Ahora puedes ir al menú 'Cálculos' para cargar el Excel con los datos del clima.")
