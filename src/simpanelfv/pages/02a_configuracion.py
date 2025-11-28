import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

st.write("""
# Configuración del sistema generador
         """)

arch_data = st.file_uploader(label='Carga Excel', accept_multiple_files=False)

if arch_data is not None:
    tabla = pd.read_excel(arch_data)
    st.dataframe(tabla)