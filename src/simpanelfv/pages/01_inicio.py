import streamlit as st

if 'config_guardada' not in st.session_state:
    st.session_state['config_guardada'] = False

if 'N' not in st.session_state:
    st.session_state['N'] = 10          # Cantidad de paneles
if 'Ppico' not in st.session_state:
    st.session_state['Ppico'] = 330.0    # Potencia pico
if 'kp' not in st.session_state:
    st.session_state['kp'] = -0.0040       # Coeficiente temperatura
if 'eta' not in st.session_state:
    st.session_state['eta'] = 0.90      # Rendimiento
if 'Pinv' not in st.session_state:
    st.session_state['Pinv'] = 3.0     # Potencia Inversor
if 'mu' not in st.session_state:
    st.session_state['mu'] = 2.0       # Umbral mínimo

# Variables de simulación (Resultados)
if 'simulacion_realizada' not in st.session_state:
    st.session_state['simulacion_realizada'] = False
st.write("""
# SimPanelFV
Simulador de generación de equipo de paneles fotovoltaicos
## Caracterísitcas de la App
## Esta aplicación contiene las siguientes características:
- Configuración Personalizada: El usuario puede ingresar manualmente las especificaciones técnicas y características operativas del sistema generador que desea simular.
- 	Configuración Predefinida: Se ofrece la opción de utilizar un perfil predefinido, basado en los parámetros técnicos del generador perteneciente a la UTN Facultad Regional Santa Fe.
### Interfaz gráfica
-	Módulo de Cálculo: Sección central de la herramienta donde el usuario configura los parámetros de entrada, como pueden ser la cantidad de módulos fotovoltaicos, parámetros de los característicos de los módulos, potencia nominal de los equipos y demás opciones y la ejecución las simulaciones del sistema.
-	Dashboard (Panel de Control): Apartado dedicado a la visualización de resultados. Presenta los datos de salida mediante gráficos, métricas y figuras de análisis dinámicas.

### Limitaciones
La aplicación basará su enfoque al analisis físico-energtico y la facilidad de su uso, por lo cual  se excluyen las siguentes funcionalidades del proyecto.

- Ánalisis Economico: No realiza cálculos de viabilidad financiera, retorno de la inversión, costos de instalación o amortización, ya que  depended de variables externas (tarifas eléctricas, costos, impuestos) que son volátiles y escapan al alcance de este simulador.

- Dimensionamiento Automático: Simpanelfv es una herramienta de simulación y validación, no de diseño o dimensionamiento automático. La aplicación no sugiere una configuración óptima de paneles basada en un perfil de consumo.
""")
