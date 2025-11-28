import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

st.write("""
# Extras
         """)

ejemplo_tabla = pd.DataFrame(data={
    "Valores": [1, 2, 3, 4, 5, 6],
    "Categorias": ["A", "B", "C", "D", "E", "F"]
})

st.dataframe(ejemplo_tabla)
fig = px.pie(ejemplo_tabla, names='Categorias', values='Valores')
st.plotly_chart(fig)