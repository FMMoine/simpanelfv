import streamlit as st

def_N = st.session_state.get('N', 10)
def_Ppico = st.session_state.get('Ppico', 330.0)
def_kp = st.session_state.get('kp', -0.0040)
def_Pinv = st.session_state.get('Pinv', 3.0)
def_eta = st.session_state.get('eta', 0.90)
def_mu = st.session_state.get('mu', 2.0)
def_Gstd = st.session_state.get('Gstd', 1000.0)
def_Tr = st.session_state.get('Tr', 25.0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Datos del Panel (FV)")
    # Cantidad de paneles
    input_N = st.number_input("Número de módulos (N)", 
                              value=def_N, step=1, min_value=1)
    # Potencia pico
    input_Ppico = st.number_input("Potencia Pico del módulo [W]", 
                                  value=def_Ppico, step=10.0, min_value=10.0)
    # Coeficiente de temperatura
    input_kp = st.number_input("Coeficiente de Temp. (kp) [1/°C]", 
                               value=def_kp, step=0.0001, format="%.4f")
    # Irradiancia Estandar
    input_Gstd = st.number_input("Irradiancia Estándar (Gstd) [W/m2]", 
                               value=def_Gstd, step=0.1, format="%.2f")
with col2:
    st.subheader("Datos del Inversor")
    # Potencia Inversor
    input_Pinv = st.number_input("Potencia Nominal Inversor [kW]", 
                                 value=def_Pinv, step=0.5, min_value=0.5)
    # Rendimiento
    input_eta = st.number_input("Rendimiento Global (eta) [0-1]", 
                                value=def_eta, step=0.01, min_value=0.01, max_value=1.0)
    # Umbral mínimo
    input_mu = st.number_input("Umbral mínimo de arranque (%)", 
                               value=def_mu, step=0.5, min_value=0.5, max_value=100.0)
    # Temperatura de referencia
    input_Tr = st.number_input("Temperatura de referencia (Tr) [°C]", 
                               value=def_Tr, step=0.1, min_value=0.0, max_value=125.0)
st.divider()

# Boton Config. Predeterminada
if st.button("Utilizar Configuración Predeterminada (Generador UTN-FRSF)"):
    st.session_state['N'] = 10
    st.session_state['Ppico'] = 330.0
    st.session_state['kp'] = -0.0040
    st.session_state['Pinv'] = 3.0
    st.session_state['eta'] = 0.90
    st.session_state['mu'] = 2.0
    st.session_state['Gstd'] = 1000.0
    st.session_state['Tr'] = 25.0

    st.session_state['config_guardada'] = True

    st.success("""Se empleará la configuración por defecto:
               \nNúmero de módulos (N): 10
               \nPotencia Pico del módulo (W): 330.0 [W]
               \nCoeficiente de Temp. (kp): -0.0040 [1/ºC]
               \nPotencia Nominal Inversor (kW): 3.0
               \nRendimiento Global (eta) [0-1]: 0.90
               \nUmbral mínimo de arranque (%): 2.0
               \nIrradiancia Estándar (Gstd) [W/m2]: 1000.0
               \nTemperatura de referencia (Tr) [°C]: 25.0
               """)
    st.info("Ahora podés ir al menú 'Datos de entrada y salida' para cargar el Excel con los datos del clima.")
# --- 3. BOTÓN DE GUARDADO ---
if st.button("Guardar Configuración", type="primary"):
    
    # Guardamos los valores que escribió el usuario
    st.session_state['N'] = input_N
    st.session_state['Ppico'] = input_Ppico
    st.session_state['kp'] = input_kp
    st.session_state['Pinv'] = input_Pinv
    st.session_state['eta'] = input_eta
    st.session_state['mu'] = input_mu
    st.session_state['Gstd'] = input_Gstd
    st.session_state['Tr'] = input_Tr
    
    st.session_state['config_guardada'] = True

    st.success("¡Configuración guardada correctamente!")
    st.info("Ahora podés ir al menú 'Datos de entrada y salida' para cargar el Excel con los datos del clima.")
