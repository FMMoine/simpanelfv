import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("📊 Análisis Gráfico Avanzado")
st.write("Visualice el comportamiento del sistema filtrando por días y horas específicas.")

if 'resultado_simulacion' not in st.session_state:
    st.warning("⚠️ No se encontraron resultados de simulación.")
    st.info("Aunque hayas cargado el Excel, necesitas ir a **'Cálculos'** y presionar el botón rojo **'Ejecutar Simulación'** para generar los datos de potencia.")
    st.stop()

# Cargamos el dataframe
df = st.session_state['resultado_simulacion'].copy()

# PROCESAMIENTO DE FECHAS
col_fecha = 'Fecha' if 'Fecha' in df.columns else df.columns[0]

try:
    df[col_fecha] = pd.to_datetime(df[col_fecha])
except Exception as e:
    st.error(f"Error al procesar las fechas en la columna '{col_fecha}'.")
    st.stop()

# BARRA LATERAL DE FILTROS 
st.sidebar.header("🔎 Filtros de Visualización")

# Definimos los límites basados en los datos
min_date = df[col_fecha].min().date()
max_date = df[col_fecha].max().date()

# Selectores de fecha
start_date = st.sidebar.date_input("Fecha de Inicio", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Fecha de Fin", max_date, min_value=min_date, max_value=max_date)

st.sidebar.divider()

# Selector de hora
hour_range = st.sidebar.slider("Rango Horario (Horas del día)", 0, 23, (0, 23))

# APLICAR FILTROS 
# Creamos la máscara de filtrado
mask = (df[col_fecha].dt.date >= start_date) & (df[col_fecha].dt.date <= end_date)
mask &= (df[col_fecha].dt.hour >= hour_range[0]) & (df[col_fecha].dt.hour <= hour_range[1])

# Aplicamos el filtro
df_filtrado = df.loc[mask]

if df_filtrado.empty:
    st.warning("⚠️ No hay datos en el rango seleccionado. Verificar que el rango de fechas se corresponde con el de los datos ingresados y que la fecha de inicio sea anterior a la última fecha analizada")
    st.info(f"Primer fecha detectada: {min_date}, Última fecha detectada: {max_date}")    
    st.stop()

st.success(f"Mostrando **{len(df_filtrado)}** registros del periodo seleccionado.")

#GRÁFICOS INTERACTIVOS

# A) Gráfico Combinado (Potencia vs Irradiancia)
st.subheader("1. Generación Eléctrica vs Recurso Solar")
fig1 = go.Figure()

# Línea de Potencia (Eje Izquierdo)
fig1.add_trace(go.Scatter(
    x=df_filtrado[col_fecha], 
    y=df_filtrado['Potencia_Salida_kW'],
    name="Potencia (kW)",
    line=dict(color='red', width=2),
    fill='tozeroy' 
))

# Línea de Irradiancia (Eje Derecho)
if 'G' in df_filtrado.columns:
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

# B) Gráfico de Barras (Energía Diaria)
st.subheader("2. Energía Diaria Acumulada (kWh)")

# Columna de día para agrupar
df_filtrado['Fecha_Dia'] = df_filtrado[col_fecha].dt.date

# Calculamos energía (Suma de potencia * tiempo).
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

# C) Gráfico de Dispersión (Eficiencia)
if 'G' in df_filtrado.columns and 'T' in df_filtrado.columns:
    with st.expander("Ver Análisis de Eficiencia (Input vs Output)"):
        st.write("Relación entre la irradiancia recibida y la potencia entregada.")
        fig3 = px.scatter(
            df_filtrado, 
            x='G', 
            y='Potencia_Salida_kW',
            color='T', 
            labels={'G': 'Irradiancia (W/m²)', 'Potencia_Salida_kW': 'Potencia (kW)', 'T': 'Temp (°C)'},
            title="Curva de Potencia vs Irradiancia"
        )
        st.plotly_chart(fig3, use_container_width=True)
