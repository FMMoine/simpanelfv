import pandas as pd
import streamlit as st

st.write("""
# Datos de entrada y configuración de la información de salida
         """)

arch_data = st.file_uploader(label='Cargar Excel', accept_multiple_files=False)

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

with st.expander("Configuraciones adicionales"):
        def_CostoInst = st.session_state.get('CostoInst', 1000000.0)
        def_CostoEn = st.session_state.get('CostoEn', 1.0)
        def_CalcAmort = st.session_state.get('CalcAmort', False)
        input_CalcAmort = st.checkbox(label="Calcular si se logra la amortización del equipo")
        # Costo de la Instalacion
        input_CostoInst = st.number_input("Costo total de la instalación (Elegir una unidad monetaria, como ARS$)", 
                              value=def_CostoInst, step=100.0, min_value=0.01)
        # Ahorro anual
        input_CostoEn = st.number_input("Costo por cada kWh, tomado como fijo (Emplear misma unidad monetaria que para el costo total)", 
                                  value=def_CostoEn, step=0.5, min_value=0.01)
        
        if st.button("Guardar Configuración", type="primary"):
    
                # Guardamos los valores que escribió el usuario
                st.session_state['CostoInst'] = input_CostoInst
                st.session_state['CostoEn'] = input_CostoEn
                st.session_state['CalcAmort'] = input_CalcAmort
                
                st.session_state['config_adicional_guardada'] = True

                st.success("¡Configuración adicional guardada correctamente!")
                st.info("Proceder con los cálculos")