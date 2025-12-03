import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("📊 Análisis Gráfico Avanzado")
st.write("Visualice el comportamiento del sistema filtrando por días y horas específicas.")


if 'df_clima' not in st.session_state:
    st.warning("No hay datos cargados. Ve a 'Datos de Entrada' y sube el Excel.")
    st.stop()

df = st.session_state['df_clima'].copy()


if 'Potencia_Salida_kW' not in df.columns:
    st.info("ℹ️ Aún no has ejecutado la simulación.")
    st.warning("Ve a la página **'Modelado'** y presiona 'Ejecutar Simulación' para generar los datos de potencia.")
    st.stop()

col_fecha = 'Fecha' if 'Fecha' in df.columns else df.columns[0]

try:
    df[col_fecha] = pd.to_datetime(df[col_fecha])
except Exception as e:
    st.error(f"Error al procesar las fechas en la columna '{col_fecha}'. Asegúrate que tenga formato de fecha válido.")
    st.stop()

#BARRA LATERAL DE FILTROS
st.sidebar.header("🔎 Filtros de Visualización")

# A) Filtro de Rango de Fechas
min_date = df[col_fecha].min().date()
max_date = df[col_fecha].max().date()

start_date = st.sidebar.date_input("Fecha de Inicio", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Fecha de Fin", max_date, min_value=min_date, max_value=max_date)

# B) Filtro de Horas (Ej. ver solo de 06:00 a 20:00)
st.sidebar.divider()
hour_range = st.sidebar.slider("Rango Horario (Horas del día)", 0, 23, (0, 23))

#  APLICAR FILTROS 
# Filtramos el dataframe 
mask = (df[col_fecha].dt.date >= start_date) & (df[col_fecha].dt.date <= end_date)
mask &= (df[col_fecha].dt.hour >= hour_range[0]) & (df[col_fecha].dt.hour <= hour_range[1])
df_filtrado = df.loc[mask]

if df_filtrado.empty:
    st.warning("No hay datos para el rango de fechas/horas seleccionado.")
    st.stop()

st.success(f"Mostrando **{len(df_filtrado)}** registros desde {start_date} hasta {end_date}.")
# GRÁFICOS INTERACTIVOS 
st.subheader("1. Generación Eléctrica vs Recurso Solar")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=df_filtrado[col_fecha], 
    y=df_filtrado['Potencia_Salida_kW'],
    name="Potencia (kW)",
    line=dict(color='red', width=2),
    fill='tozeroy' 
))


fig1.add_trace(go.Scatter(
    x=df_filtrado[col_fecha], 
    y=df_filtrado['G'],
    name="Irradiancia (W/m²)",
    line=dict(color='orange', width=1, dash='dot'),
    yaxis="y2"
))
fig1.update_layout(
    xaxis_title="Tiempo",
    yaxis=dict(title="Potencia Generada (kW)"),
    yaxis2=dict(title="Irradiancia (W/m²)", overlaying="y", side="right"),
    legend=dict(x=0, y=1.1, orientation="h"),
    height=500,
    hovermode="x unified" 
)
st.plotly_chart(fig1, use_container_width=True)
st.subheader("2. Energía Diaria Acumulada (kWh)")

df_filtrado['Fecha_Dia'] = df_filtrado[col_fecha].dt.date
energia_diaria = df_filtrado.groupby('Fecha_Dia')['Potencia_Salida_kW'].sum() * (10/60)
df_energia = energia_diaria.reset_index(name='Energia_kWh')

fig2 = px.bar(
    df_energia, 
    x='Fecha_Dia', 
    y='Energia_kWh',
    labels={'Fecha_Dia': 'Fecha', 'Energia_kWh': 'Energía (kWh)'},
    color='Energia_kWh',
    color_continuous_scale='Blues'
)
fig2.update_layout(height=400)
st.plotly_chart(fig2, use_container_width=True)

with st.expander("Ver Análisis de Eficiencia (Input vs Output)"):
    st.write("Este gráfico muestra qué tan bien convierte el panel la luz en electricidad. Una línea recta indica buen funcionamiento; una 'meseta' indica recorte del inversor.")
    fig3 = px.scatter(
        df_filtrado, 
        x='G', 
        y='Potencia_Salida_kW',
        color='T', 
        labels={'G': 'Irradiancia (W/m²)', 'Potencia_Salida_kW': 'Potencia Salida (kW)', 'T': 'Temp (°C)'},
        title="Curva de Potencia vs Irradiancia"
    )
    st.plotly_chart(fig3, use_container_width=True)
