![simpanelfv brand](img/SimpanelFVBrand.png)

# simpanelfv
Este es un Proyecto Integrador de Introduccion a la programacion cientifica con MatLab y Python, ABP. 
Se basa en un Simulador Generador Fotovoltaico

## Tabla de contenidos
* [Memoria Descriptiva](#memoria-descriptiva)
* [Caracterísitcas de la App](#caracterísitcas-de-la-app)
    * [Interfaz gráfica](#interfaz-gráfica)
    * [Limitaciones](#limitaciones)
* [License](#license)
* [Autores](#Autores)
* [Link](#Link) 

## [Memoria Descriptiva](memoria_descriptiva.pdf)

## Caracterísitcas de la App
Esta aplicación contiene las siguientes características:
- Configuración Personalizada: El usuario puede ingresar manualmente las especificaciones técnicas y características operativas del sistema generador que desea simular.
- 	Configuración Predefinida: Se ofrece la opción de utilizar un perfil predefinido, basado en los parámetros técnicos del generador perteneciente a la UTN Facultad Regional Santa Fe.
### Interfaz gráfica
-	Módulo de Cálculo: Sección central de la herramienta donde el usuario configura los parámetros de entrada, como pueden ser la cantidad de módulos fotovoltaicos, parámetros de los característicos de los módulos, potencia nominal de los equipos y demás opciones y la ejecución de las simulaciones del sistema.
-	Dashboard (Panel de Control): Apartado dedicado a la visualización de resultados. Presenta los datos de salida mediante gráficos, métricas y figuras de análisis dinámicas.

### Limitaciones
La aplicación basará su enfoque al analisis físico-energtico y la facilidad de su uso, por lo cual  se excluyen las siguentes funcionalidades del proyecto.

- Ánalisis Economico: No realiza cálculos de viabilidad financiera, retorno de la inversión, costos de instalación, ya que  depende de variables externas (tarifas eléctricas, costos, impuestos) que son volátiles y escapan al alcance de este simulador. Posee un apartado simplificado para estimar si el ahorro en la energía generada supera el costo de la instalación para el período completo de generación.

- Dimensionamiento Automático: Simpanelfv es una herramienta de simulación y validación, no de diseño o dimensionamiento automático. La aplicación no sugiere una configuración óptima de paneles basada en un perfil de consumo.

## License
MIT License
Copyright (c) 2025 Simpanelfv

# Autores
- Francisco Moine: fmoine@frsf.utn.edu.ar
- Gonzalo Morel: gmorel@frsf.utn.edu.ar
- Leonel Oldrini: loldrini@frsf.ut.edu.ar
## Link
https://simpanelfv-utn-frsf.streamlit.app/

![simpanelfv flyer](img/SimpanelFV1.png)
