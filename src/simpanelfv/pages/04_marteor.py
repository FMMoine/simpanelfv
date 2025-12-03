import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from lib.fcn_base import lib_test, GenPanFV
st.write ("""
# Sistema de un generador fotovoltaico
Un Un generador de energía fotovoltaica (o sistema solar fotovoltaico) es una instalación 
eléctrica diseñada para transformar la radiación solar en electricidad utilizable mediante 
el efecto fotoeléctrico.
## Funcionamiento
El proceso sigue un flujo lineal de conversión de energía:
 - Captación (DC): Los fotones de la luz solar impactan sobre las células del material 
 semiconductor de los paneles. Esto excita los electrones, generando una corriente continua (DC).
 - Regulación: Si hay baterías, un controlador gestiona el voltaje y amperaje para protegerlas.
 - Inversión (DC $\to$ AC): La corriente continua no sirve para la mayoría de electrodomésticos 
 ni para la red. Un inversor transforma esa onda continua en una onda alterna (senoidal pura, 
 generalmente a 220V/50Hz en Argentina).Distribución: La energía alterna alimenta el tablero 
 principal de la vivienda.
 ## Componentes Clave del Circuito
- Paneles Solares (Módulos): Arreglos de celdas (generalmente de silicio monocristalino 
o policristalino) conectados en serie o paralelo para alcanzar el voltaje de diseño del sistema.
- Inversor: El "cerebro" del sistema. Sincroniza la frecuencia de la onda generada con la de 
la red eléctrica (en sistemas conectados) o crea su propia onda de referencia (en sistemas 
aislados). Los inversores modernos también incluyen MPPT (Seguidores del Punto de Máxima Potencia)
para optimizar la eficiencia del panel bajo sombras parciales.
- Baterías (Acumuladores): Esenciales solo en sistemas aislados o híbridos. Almacenan energía 
química (Litio o Plomo-Ácido) para usarla cuando no hay sol.
- Regulador de Carga: Se coloca entre los paneles y las baterías para evitar sobrecargas o
descargas profundas que dañen los bancos de baterías. 
## Consideraciones a tener en cuenta
- Factor de Potencia: Al igual que en los circuitos industriales que te interesan,
los inversores deben gestionar el factor de potencia para entregar energía eficiente.
- Dimensionamiento: No se trata solo de poner paneles. Debes calcular tu consumo en kWh/mes 
y la irradiación solar de tu zona (HSP: Horas Sol Pico) para determinar cuántos paneles 
y baterías necesitas.
""")
