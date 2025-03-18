import streamlit as st
import pandas as pd
import numpy as np
from models.acuerdo006 import Acuerdo006Calculator
from utils.visualizations import plot_salary_evolution

# Set page configuration
st.set_page_config(
    page_title="Simulador de Salarios Docentes UPC",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page title
st.title("Calculadora de Salarios Docentes UPC")
st.subheader("Herramienta de Simulación y Análisis")

# Introduction
st.markdown("""
## Bienvenido al Simulador de Salarios Docentes UPC

Esta aplicación te permite:
1. Calcular salarios de profesores ocasionales según el Acuerdo 006 de 2018
Utiliza la barra lateral para navegar a través de las diferentes funcionalidades.
""")

st.markdown("""
### Acuerdo 006 de 2018
El Acuerdo 006 regula la contratación y pago de profesores ocasionales en la UPC, basado en:
- Títulos académicos
- Categoría
- Horas de docencia
- Experiencia
""")

st.markdown("## Ejemplo de Evolución Salarial")
sample_data = pd.DataFrame({
    'Año': list(range(2022, 2032)),
    'Salario Base': [4000000 * (1.04)**i for i in range(10)],
    'Con Bonificación por Productividad': [4000000 * (1.04)**i * 1.15 for i in range(10)]
})

st.line_chart(
    sample_data.set_index('Año')
)
st.markdown("""
Desarrollado para UPC
""")

st.markdown("---")
st.markdown("© 2025 Simulador de Salarios Docentes UPC")

st.markdown("### *I am inevitable.* 🟣")
