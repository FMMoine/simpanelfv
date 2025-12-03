import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

st.write("""
# Cálculos y Resultados
Simulación del rendimiento energético del generador configurado.
""")

if not st.session_state.get('config_guardada'):
    st.warning("No has configurado el equipo.")
    st.info("Ve a 'Generador Fotovoltaico' (menú lateral) y guarda los parámetros.")
    st.stop()

if 'df_clima' not in st.session_state:
    st.warning("No has cargado los datos meteorológicos.")
    st.info("Ve a 'Datos de Entrada y Salida' (menú lateral) y sube el Excel.")
    st.stop()

N = st.session_state['N']
Ppico = st.session_state['Ppico']
kp = st.session_state['kp']
Pinv = st.session_state['Pinv']
eta = st.session_state['eta']
mu = st.session_state['mu']


df = st.session_state['df_clima']

st.success(f"Datos listos: Simular {N} paneles ({Ppico}W) con {len(df)} registros de clima.")

if st.button("Ejecutar Simulación", type="primary"):
    
    with st.spinner("Calculando potencia generada..."):

        generador = GenPanFV(Ppico=Ppico, N=N, kp=kp, eta=eta, Pinv=Pinv, mu=mu)

        potencias = generador.pot_generada_rango(df['G'], df['T'])
        

        df['Potencia_Salida_kW'] = potencias
         
         #resultados
        st.divider()
        st.subheader("Métricas de Rendimiento")
           #Columnas
        col1, col2, col3 = st.columns(3)
        col1.metric("Energía Total Generada", f"{generador.energia():.2f} kWh")
        col2.metric("Potencia Máxima", f"{generador.max_pot()[1]:.2f} kW")
        col3.metric("Factor de Utilización", f"{generador.factor_de_utilizacion()*100:.2f} %")
        
        # Gráfico 
        st.subheader("Curva de Potencia")
        col_x = 'Fecha' if 'Fecha' in df.columns else df.columns[0]
        fig = px.line(
            df, 
            x=col_x, 
            y='Potencia_Salida_kW',
            title='Perfil de Generación de Potencia',
            labels={col_x: 'Tiempo', 'Potencia_Salida_kW': 'Potencia (kW)'}
        )
        
        # Personalización:
        fig.update_traces(line_color='red', fill='tozeroy')
        fig.update_layout(hovermode="x unified") # Muestra el valor al pasar el mouse
        
        st.plotly_chart(fig, use_container_width=True)
      
        
        # Tabla de datos
        with st.expander("Ver tabla de resultados detallada"):
            st.dataframe(df)

        # Botón para descargar resultados
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Resultados en CSV",
            data=csv,
            file_name='resultados_simulacion.csv',
            mime='text/csv',
        )
