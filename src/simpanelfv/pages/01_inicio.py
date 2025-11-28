import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV

st.write("""
        # SimPanelFV
        Simulador de generación de equipo de paneles fotovoltaicos
 ## Caracterísitcas de la App
## Esta aplicación contiene las siguientes características:
- Configuración Personalizada: El usuario puede ingresar manualmente las especificaciones técnicas y características operativas del sistema generador que desea simular.
- 	Configuración Predefinida: Se ofrece la opción de utilizar un perfil predefinido, basado en los parámetros técnicos del generador perteneciente a la UTN Facultad Regional Santa Fe.
### Interfaz gráfica
-	Módulo de Cálculo: Sección central de la herramienta donde el usuario configura los parámetros de entrada, como pueden ser la cantidad de módulos fotovoltaicos, parámetros de los característicos de los módulos, potencia nominal de los equipos y demás opciones y la ejecución las simulaciones del sistema.
-	Dashboard (Panel de Control): Apartado dedicado a la visualización de resultados. Presenta los datos de salida mediante gráficos, métricas y figuras de análisis dinámicas.

### Limitaciones
La aplicación basará su enfoque al analisis físico-energtico y la facilidad de su uso, por lo cual  se excluyen las siguentes funcionalidades del proyecto.

- Ánalisis Economico: No realiza cálculos de viabilidad financiera, retorno de la inversión, costos de instalación o amortización, ya que  depended de variables externas (tarifas eléctricas, costos, impuestos) que son volátiles y escapan al alcance de este simulador.

- Dimensionamiento Automático: Simpanelfv es una herramienta de simulación y validación, no de diseño o dimensionamiento automático. La aplicación no sugiere una configuración óptima de paneles basada en un perfil de consumo.

- Análisis de Sombras y "Balance of System" (BOS): La simulación no contempla pérdidas de rendimiento ocasionadas por sombreado de objetos externos. Asimismo, el cálculo se centra en el rendimiento ideal del panel basado en la irradiancia y los datos del fabricante, sin simular las pérdidas específicas de componentes eléctricos del BOS.
 """)