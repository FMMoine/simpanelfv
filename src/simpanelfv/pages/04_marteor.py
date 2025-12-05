import streamlit as st

st.write("""
# Sistema de un generador fotovoltaico
Un generador de energía fotovoltaica (o sistema solar fotovoltaico) es una instalación 
eléctrica diseñada para transformar la radiación solar en electricidad utilizable mediante 
el efecto fotoeléctrico.
""")

st.write("""
## Funcionamiento
El proceso sigue un flujo lineal de conversión de energía: 
* **Captación (DC):** Los fotones de la luz solar impactan sobre las células del material 
semiconductor de los paneles. Esto excita los electrones, generando una corriente continua (DC).
* **Regulación:** Si hay baterías, un controlador gestiona el voltaje y amperaje para protegerlas.
* **Inversión (DC $\\to$ AC):** La corriente continua no sirve para la mayoría de electrodomésticos 
ni para la red. Un inversor transforma esa onda continua en una onda alterna (senoidal pura, 
generalmente a 220V/50Hz en Argentina).
* **Distribución:** La energía alterna alimenta el tablero principal de la vivienda.

## Componentes clave del circuito
* **Paneles Solares (Módulos):** Arreglos de celdas (generalmente de silicio monocristalino 
o policristalino) conectados en serie o paralelo para alcanzar el voltaje de diseño del sistema.
* **Inversor:** El "cerebro" del sistema. Sincroniza la frecuencia de la onda generada con la de 
la red eléctrica (en sistemas conectados) o crea su propia onda de referencia (en sistemas 
aislados). Los inversores modernos también incluyen MPPT para optimizar la eficiencia.
* **Baterías (Acumuladores):** Esenciales solo en sistemas aislados o híbridos.
* **Regulador de Carga:** Se coloca entre los paneles y las baterías.

## Consideraciones a tener en cuenta
* **Factor de Potencia:** Al igual que en los circuitos industriales, los inversores deben gestionar el factor de potencia.
* **Dimensionamiento:** Debes calcular tu consumo en kWh/mes y la irradiación solar (HSP).
""")

st.write("## Fórmulas del cálculo")

st.subheader("Potencia Eléctrica Generada [kW]")
st.latex(r"""P[\text{kW}] = N \cdot \frac{G}{G_{\text{std}}} \cdot P_{\text{pico}} \cdot \left[ 1 + k_p \cdot (T_c - T_r) \right] \cdot \eta \cdot 10^{-3}""")

st.write("Donde:")

# Usamos st.markdown para poder escribir las variables con LaTeX integrado ($variable$)
st.markdown(r"""
* $N$: Cantidad total de paneles en el arreglo.
* $G$: Irradiancia global incidente ($W/m^2$). Mide el flujo de energía solar.
* $G_{std}$: Irradiancia estándar. Normalmente $G_{std} = 1000 [W/m^2]$.
* $T_r$: Temperatura de referencia ($^\circ C$). Normalmente $T_r = 25 [^\circ C]$.
* $T_c$: Temperatura de la celda ($^\circ C$).
* $P_{pico}$: Potencia pico de cada módulo ($W$). Es la potencia cuando $G$ coincide con $G_{std}$ y $T_c$ con $T_r$.
* $k_p$: Coeficiente de temperatura-potencia ($^\circ C^{-1}$). Es negativo; si $T_c$ sube, $P$ baja.
* $\eta$: Rendimiento global de la instalación "por unidad" (valor ideal: 1). Incluye suciedad, sombras y rendimiento del inversor.
""")

st.subheader("Temperatura de la celda")
st.latex(r"""T_c = T + 0.031 \left[^\circ C \, m^2/W \right] \cdot G""")

st.markdown(r"""
Donde:
* $T_c$: La Temperatura de la celda en $[^\circ C]$.
* $G$: Irradiancia global incidente ($W/m^2$).
""")

st.subheader("Límites de generación (Inversor)")
st.markdown(r"""
Los circuitos inversores funcionan adecuadamente siempre que la producción supere un umbral mínimo $\mu$ (\%).
Asimismo, el valor $P_{inv}$ opera como límite superior (clipping).
""")

st.latex(r"""P_{\min} [kW] = \frac{\mu(\%)}{100} \cdot P_{inv}""")

st.latex(r"""P_r [kW] = 
\begin{cases} 
0 & \text{si } P \leq P_{\min} \\
P & \text{si } P_{\min} < P \leq P_{inv} \\
P_{inv} & \text{si } P > P_{inv}
\end{cases}""")
