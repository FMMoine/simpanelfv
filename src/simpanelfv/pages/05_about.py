import streamlit as st

st.write("""
    # Miembros y Contactos:
- Francisco Moine: fmoine@frsf.utn.edu.ar
- Gonzalo Morel: gmorel@frsf.utn.edu.ar
- Leonel Oldrini: loldrini@frsf.ut.edu.ar

## MIT License Copyright (c) 2025 Simpanelfv

### Repositorio Github de Acceso Público, Disponible en: https://github.com/FMMoine/simpanelfv

            """)

if st.button(label='Presiona para contenido adicional', type="primary"):
    st.balloons()
    with st.popover("Otro curioso que presiona el botón"):
        st.markdown("Son 17 ya")
