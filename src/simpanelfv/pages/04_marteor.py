import streamlit as st

st.write ("""
# Sistema de un generador fotovoltaico
Un generador de energía fotovoltaica (o sistema solar fotovoltaico) es una instalación 
eléctrica diseñada para transformar la radiación solar en electricidad utilizable mediante 
el efecto fotoeléctrico. """)
st.write ("""## Funcionamiento
El proceso sigue un flujo lineal de conversión de energía: 
 - Captación (DC): Los fotones de la luz solar impactan sobre las células del material 
 semiconductor de los paneles. Esto excita los electrones, generando una corriente continua (DC).
 - Regulación: Si hay baterías, un controlador gestiona el voltaje y amperaje para protegerlas.
 - Inversión (DC $\to$ AC): La corriente continua no sirve para la mayoría de electrodomésticos 
 ni para la red. Un inversor transforma esa onda continua en una onda alterna (senoidal pura, 
 generalmente a 220V/50Hz en Argentina).Distribución: La energía alterna alimenta el tablero 
 principal de la vivienda. 
 ## Componentes clave del circuito
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

## Formulas del cáculo
### Potencia Eléctrica Generada [Kw].""")
st. latex (r"""P[\text{kW}] = N \cdot \frac{G}{G_{\text{std}}} \cdot P_{\text{pico}} \cdot \left[ 1 + k_p \cdot (T_c - T_r) \right] \cdot \eta \cdot 10^{-3}""")

st.write("""donde:""")
- st.latex(r"""N"""):st.write("""Cantidad total de paneles en el arreglo.""")
- st.latex(r"""G"""): st.write("""Irradiancia global incidente en forma normal a los módulos fotovoltaicos, en W/m2.
La irradiancia mide el flujo de energía proveniente de la radiación solar (sea de forma
directa o indirecta) por unidad de superficie incidente.""")
- st.latex(r"""G_{std}"""):st.write(""" Irradiancia estándar, en W/m2. Es un valor de irradiancia que utilizan los fabricantes
de los módulos para referenciar ciertas características técnicas. Normalmente """)
- st.latex(r"""G_{std} = 1000 [W/m2]""").
- st.latex(r"""T_r"""): st.write("""Temperatura de referencia, en Celsius. Es una temperatura utilizada por los
fabricantes de los módulos para referenciar ciertos parámetros que dependen de la
misma. Normalmente""") st.latex(r"""T_r = 25 [◦C])""").
- st.latex(r"""T_c"""):st.write(""" Temperatura de la celda, en Celsius. Es la temperatura de los componentes
semiconductores que conforman cada módulo fotovoltaico.""")
- st.latex(r"""P_{pico}"""): st.write("""Potencia pico de cada módulo, en Watt. Se interpreta como la potencia eléctrica
que entrega un módulo cuando""") st.latex(r"""G""") st.write("""coincide con""") st.latex(r"""G_{std}""") 
st.write("""y cuando""") st.latex(r"""T_c""") st.write("""coincide con""") st.latex(r"""T_r""")st.write(""", en
ausencia de viento y sin que el panel se vincule a otros componentes eléctricos que
afecten el desempeño de la instalación. Constituye la potencia nominal bajo la cual
los módulos son comercializados.""")
- st.latex(r"""kp"""):st.write(""" Coeficiente de temperatura-potencia, en""") st.latex(r"""◦C^{−1}"""). st.write("""Es un parámetro negativo que
refleja cómo incide la temperatura de la celda en el rendimiento del""") st.latex(r"""GFV""").st.write(""" Se observa
que incrementos (disminuciones) de""") st.latex(r"""T_c""") st.write("""producen, en consecuencia, disminuciones
(incrementos) de""") st.latex(r"""P""").
- st.latex(r"""η"""): st.write("""Rendimiento global de la instalación “por unidad” (valor ideal:""") st.latex(1)st.write("""). Se utiliza para
considerar el efecto de sombras parciales sobre el""") st.latex(r"""GFV""")st.write(""", suciedad sobre la superficie
de los módulos y, fundamentalmente, el rendimiento del equipo controlador-inversor.
Los inversores contemplados por el modelo también incluyen el sistema 
de control para maximizar la potencia de salida.

### Temperatura de la celda""")

st.latex(r"""T_c = T + 0.031 \left[^\circ C \, m^2/W \right] \cdot G""")
st.write("""donde:""")
- st.latex(r"""T_c"""): st.write("""La Temperatura de la celda en""") st.latex(r"""[°C]""").
- st.latex(r"""G"""): st.write("""Irradiancia global incidente en forma normal a los módulos fotovoltaicos, en""") st.latex(r"""W/m^2""").
st.write("""La irradiancia mide el flujo de energía proveniente de la radiación solar (sea de forma
directa o indirecta) por unidad de superficie incidente.

### Limites de generación.
Los circuitos inversores funcionan adecuadamente siempre que la producción, en términos
de potencia, supere un umbral mínimo""") st.latex(r"""μ""")st.write(""", habitualmente expresado en forma porcentual,
en relación a la potencia nominal""") st.latex(r"""P_{inv}""") st.write("""del equipo. Si este umbral no es superado, la instalación
no entrega potencia eléctrica. Asimismo, el valor""") st.latex(r"""P_{inv}""") st.write("""(en kilo-Watt) opera como
límite superior del""") st.latex(r"""GFV"""). st.write("""En consecuencia, la potencia real Pr que entrega la instalación se
puede calcular como:""")

st.latex(r"""P_{\min} [kW] = \frac{\mu(\%)}{100} \cdot P_{inv}""")

st.latex(r"""P_r [kW] = 
\begin{cases} 
0 & \text{si } P \leq P_{\min} \\
P & \text{si } P_{\min} < P \leq P_{inv} \\
P_{inv} & \text{si } P > P_{inv}
\end{cases}""")

