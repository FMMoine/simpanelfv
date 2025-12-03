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
        potencias = generador.pot_generada_rango(df_input['G'], df_input['T'])

       # Crear copia
        df_resultado = df_input.copy()
        df_resultado['Potencia_Salida_kW'] = potencias
        
        # GUARDAR
        st.session_state['resultado_simulacion'] = df_resultado
        st.session_state['simulacion_lista'] = True

#VISUALIZACIÓN Y FILTROS 
if st.session_state.get('simulacion_lista'):
    df = st.session_state['resultado_simulacion']
    st.divider()
    st.subheader("🔍 Análisis de Resultados")
    
    with st.expander("Filtros de Fecha y Hora", expanded=True):
        col_filtro1, col_filtro2 = st.columns(2)
        col_fecha = 'Fecha' if 'Fecha' in df.columns else df.columns[0]
        try:
            df[col_fecha] = pd.to_datetime(df[col_fecha])
        except:
            st.error("No se pudo detectar el formato de fecha.")
            st.stop()

        #  Filtro de Fechas
        min_date = df[col_fecha].min().date()
        max_date = df[col_fecha].max().date()
        
        with col_filtro1:
            start_date = st.date_input("Fecha Inicio", min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("Fecha Fin", max_date, min_value=min_date, max_value=max_date)

        #  Filtro de Horas
        with col_filtro2:
            hora_rango = st.slider("Rango Horario", 0, 23, (6, 20)) # Por defecto de 6am a 8pm
        
        # APLICAR FILTROS
        mask = (df[col_fecha].dt.date >= start_date) & (df[col_fecha].dt.date <= end_date)
        mask &= (df[col_fecha].dt.hour >= hora_rango[0]) & (df[col_fecha].dt.hour <= hora_rango[1])
        
        df_filtrado = df.loc[mask]
        
        if df_filtrado.empty:
            st.warning("⚠️ No hay datos en el rango seleccionado.")
            st.stop()

    
    energia_filtrada = df_filtrado['Potencia_Salida_kW'].sum() * (10/60)
    pot_max_filtrada = df_filtrado['Potencia_Salida_kW'].max()
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
