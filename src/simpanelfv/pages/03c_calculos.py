import pandas as pd
import streamlit as st

import streamlit as st
from io import BytesIO

st.write("""
# Descarga de Recursos
Acá podés obtener la plantilla necesaria para cargar tus datos meteorológicos.
""")

st.subheader("Plantilla de Datos")
st.write("Descarga este archivo Excel de ejemplo para ver el formato correcto (columnas G y T).")

#CREAR DATOS DE EJEMPLO
df_ejemplo = pd.DataFrame({
    'Fecha': ['01/01/2024 12:00', '01/01/2024 12:10', '01/01/2024 12:20'],
    'G': [800, 950, 1000],  # Irradiancia
    'T': [25, 27, 30]       # Temperatura
})

st.table(df_ejemplo)

# GENERAR EL ARCHIVO EXCEL 
try:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_ejemplo.to_excel(writer, index=False, sheet_name='Datos_Clima')
    
    data_excel = output.getvalue()
        # BOTÓN DE DESCARGA 
    st.download_button(
        label="Descargar Plantilla Excel (.xlsx)",
        data=data_excel,
        file_name="plantilla_clima_ejemplo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

except Exception as e:
    # Si falla la creación del Excel, ofrecemos CSV
    st.warning("Nota: Se descargará en formato CSV por compatibilidad del servidor.")
    csv = df_ejemplo.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Plantilla CSV",
        data=csv,
        file_name="plantilla_clima.csv",
        mime="text/csv"
    )
