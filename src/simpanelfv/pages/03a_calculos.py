import pandas as pd
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

st.write("""
# Cálculos y Resultados
Simulación del rendimiento energético del generador configurado.
""")


if not st.session_state.get('config_guardada'):
    st.warning("⚠️ No has configurado el equipo.")
    st.info("Ve a 'Generador Fotovoltaico' (menú lateral) y guarda los parámetros.")
    st.stop()

if 'df_clima' not in st.session_state:
    st.warning("⚠️ No has cargado los datos meteorológicos.")
    st.info("Ve a 'Datos de Entrada y Salida' (menú lateral) y sube el Excel.")
    st.stop()


N = st.session_state['N']
Ppico = st.session_state['Ppico']
kp = st.session_state['kp']
Pinv = st.session_state['Pinv']
eta = st.session_state['eta']
mu = st.session_state['mu']


df_input = st.session_state['df_clima'] 

st.success(f"✅ Datos listos: Simular {N} paneles ({Ppico}W) con {len(df_input)} registros de clima.")


if st.button("Ejecutar Simulación", type="primary"):
    
    with st.spinner("Calculando potencia generada..."):
        
        generador = GenPanFV(Ppico=Ppico, N=N, kp=kp, eta=eta, Pinv=Pinv, mu=mu)
        
        
        potencias = generador.pot_generada_rango(df_input['G'], df_input['T'])
        
       
        df_resultado = df_input.copy()
        df_resultado['Potencia_Salida_kW'] = potencias
        
      
        st.session_state['resultado_simulacion'] = df_resultado
        st.session_state['simulacion_lista'] = True


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

        
        min_date = df[col_fecha].min().date()
        max_date = df[col_fecha].max().date()
        
        with col_filtro1:
            start_date = st.date_input("Fecha Inicio", min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("Fecha Fin", max_date, min_value=min_date, max_value=max_date)

        # Rango de horas
        with col_filtro2:
            hora_rango = st.slider("Rango Horario", 0, 23, (6, 20)) 
        
        # APLICAR FILTROS
        mask = (df[col_fecha].dt.date >= start_date) & (df[col_fecha].dt.date <= end_date)
        mask &= (df[col_fecha].dt.hour >= hora_rango[0]) & (df[col_fecha].dt.hour <= hora_rango[1])
        
        df_filtrado = df.loc[mask]
        
        if df_filtrado.empty:
            st.warning("⚠️ No hay datos en el rango seleccionado.")
            st.stop()

   
    
    energia_filtrada = df_filtrado['Potencia_Salida_kW'].sum() * (10/60)
    pot_max_filtrada = df_filtrado['Potencia_Salida_kW'].max()
    

    horas_totales = len(df_filtrado) * (10/60)
    energia_ideal = Pinv * horas_totales
    fu_filtrado = (energia_filtrada / energia_ideal * 100) if energia_ideal > 0 else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Energía (Filtrada)", f"{energia_filtrada:.2f} kWh")
    c2.metric("Potencia Máx", f"{pot_max_filtrada:.2f} kW")
    c3.metric("Factor de Uso", f"{fu_filtrado:.1f} %")

    #GRÁFICO 
    st.subheader("Curva de Potencia")
    
    fig = px.line(
        df_filtrado, 
        x=col_fecha, 
        y='Potencia_Salida_kW',
        title=f'Generación ({start_date} al {end_date})',
        labels={col_fecha: 'Tiempo', 'Potencia_Salida_kW': 'Potencia (kW)'}
    )
    fig.update_traces(line_color='red', fill='tozeroy')
    fig.update_layout(hovermode="x unified") 
    
    st.plotly_chart(fig, use_container_width=True)
    
    #DESCARGA
    with st.expander("Ver tabla de datos"):
        st.dataframe(df_filtrado)
        
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV Filtrado", csv, "simulacion_filtrada.csv", "text/csv")
