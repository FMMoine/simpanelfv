# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
import streamlit as st

from lib.fcn_base import lib_test

# lib_test()

pages = {
    "Información General": [
        st.Page("pages/01_inicio.py", title="Inicio"),
        st.Page("pages/04_marteor.py", title="Marco Teórico"),
        st.Page("pages/05_about.py", title="Learn about us"),
    ],

    "Configuración": [
        st.Page("pages/02a_configuracion.py", title="Generador Fotovoltaico"),
        st.Page("pages/02b_configuracion.py", title="Datos de Entrada y Salida"),
    ],

    "Cálculos": [
        st.Page("pages/03a_calculos.py", title="Modelado"),
        st.Page("pages/03b_calculos.py", title="Gráficos"),
        st.Page("pages/03c_calculos.py", title="Extras"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
