# Modulo de prueba auxiliar

import fcn_base as fcn  # Importa el módulo que acabamos de crear
import matplotlib.pyplot as plt
import numpy as np

# --- 1. DATOS DE ENTRADA (EJEMPLO) ---
# Vamos a simular 3 horas (18 mediciones cada 10 minutos)
# Lista de Irradiancia (G) en W/m²
lista_G = [0, 50, 100, 200, 400, 600, 700, 800, 850, 800, 700, 600, 400, 200, 100, 50, 0, 0]
# Lista de Temperatura (T) en °C
lista_T = [18, 18, 19, 19, 20, 21, 22, 23, 24, 24, 23, 22, 21, 20, 19, 19, 18, 18]

# Parámetros del Generador Fotovoltaico
Ppico = 240     # Potencia pico de un módulo (W)
N = 12          # Número de módulos
kp = -0.0044    # Coeficiente de temperatura (1/°C)
eta = 0.97      # Rendimiento (inversor, cableado, etc.)
Pinv = 2.5      # Potencia nominal del inversor (kW)
mu = 2          # Umbral porcentual mínimo del inversor (%)
Gstd = 1000     # Irradiancia estándar (W/m²)
Tr = 25         # Temperatura de referencia (°C)

print("--- Ejecutando test del simulador GFV ---")

# --- 2. PRUEBA DE LAS FUNCIONES ---

# Probar la función de testeo
fcn.lib_test()

# Probar 'pot_media'
P_media = fcn.pot_media(lista_G, lista_T, N, Ppico, eta, kp, Pinv, mu, Gstd, Tr)
print(f"\n[Resultados de la Simulación]")
print(f"Potencia Media: {P_media:.2f} kW")

# Probar 'energia'
E_total = fcn.energia(lista_G, lista_T, N, Ppico, eta, kp, Pinv, mu, Gstd, Tr)
print(f"Energía Total Generada: {E_total:.2f} kWh")

# Probar 'factor_de_utilizacion'
FDU = fcn.factor_de_utilizacion(lista_G, lista_T, N, Ppico, eta, kp, Pinv, mu, Gstd, Tr)
print(f"Factor de Utilización (vs Inversor): {FDU:.2%}")

# Probar 'max_pot'
P_max_tupla = fcn.max_pot(lista_G, lista_T, N, Ppico, eta, kp, Pinv, mu, Gstd, Tr)
print(f"Potencia Máxima: {P_max_tupla[1]:.2f} kW (ocurrió en el índice {P_max_tupla[0]})")

# Probar 'pot_modelo_GFV' (para un solo punto)
# --- CORRECCIÓN AQUÍ ---
# El error estaba en esta línea. Faltaba Ppico= y N= estaba mal.
P_punto_max = fcn.pot_modelo_GFV(G=850, T=24, N=N, Ppico=Ppico, eta=eta, kp=kp, Pinv=Pinv, mu=mu, Gstd=Gstd, Tr=Tr)
# --- FIN DE LA CORRECCIÓN ---
print(f"Cálculo puntual (G=850, T=24): {P_punto_max:.2f} kW")

# --- 3. PRUEBA DEL GRÁFICO ---
print("\nGenerando gráfico (cierre la ventana para finalizar)...")
figura = fcn.graficar_pot(lista_G, lista_T, N, Ppico, eta, kp, Pinv, mu, Gstd, Tr)

# Mostrar el gráfico en una ventana emergente
plt.show()

print("--- Test finalizado ---")