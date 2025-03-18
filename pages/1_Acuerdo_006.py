import streamlit as st
import pandas as pd
import numpy as np
from models.acuerdo006 import Acuerdo006Calculator
from utils.visualizations import plot_salary_evolution

st.set_page_config(
    page_title="Simulador de Salarios Profesores Ocasionales UPC",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Acuerdo 006 - Calculadora de Salarios para Profesores Ocasionales")

# Initialize calculator
acuerdo006_calculator = Acuerdo006Calculator()

# Create two columns for input and output
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Variables de Entrada")
    
    # Highest academic degree
    highest_degree = st.selectbox(
        "Título Académico más Alto",
        ["Pregrado", "Especialización", "Maestría", "Doctorado"],
        help="El título académico más alto obtenido por el profesor"
    )
    
    # Dedication type
    dedication_type = st.selectbox(
        "Tipo de Dedicación",
        ["Tiempo Completo", "Medio Tiempo", "Hora Cátedra"],
        help="Tipo de dedicación (Tiempo completo, medio tiempo o por horas)"
    )
    
    # Weekly hours (only for Hora Cátedra)
    weekly_hours = None
    if dedication_type == "Hora Cátedra":
        weekly_hours = st.slider(
            "Horas Semanales",
            min_value=1,
            max_value=19,
            value=8,
            help="Número de horas semanales de enseñanza (solo para Hora Cátedra)"
        )
    
    # Experience years
    experience_years = st.slider(
        "Años de Experiencia Académica",
        min_value=0,
        max_value=30,
        value=3,
        help="Número de años de experiencia académica"
    )
    
    # Base year
    base_year = st.number_input(
        "Año Base",
        min_value=2020,
        max_value=2030,
        value=2024
    )
    
    # Projection years
    projection_years = st.slider(
        "Años de Proyección",
        min_value=1,
        max_value=20,
        value=10,
        help="Número de años para proyectar el salario"
    )
    
    # Prepare input data
    input_data = {
        "highest_degree": highest_degree,
        "dedication_type": dedication_type,
        "weekly_hours": weekly_hours,
        "experience_years": experience_years,
        "base_year": base_year,
        "projection_years": projection_years
    }
    
    # Calculate button
    st.markdown("---")
    calculate_button = st.button("Calcular Salario", type="primary")

# Output column
with col2:
    st.header("Resultados del Cálculo")
    
    if calculate_button:
        # Calculate salary
        results = acuerdo006_calculator.calculate_salary(input_data)
        
        # Display hourly rate and weekly hours
        col_rate, col_hours = st.columns(2)
        with col_rate:
            st.metric("Tarifa por Hora", f"${results['hourly_rate']:,.0f} COP")
        with col_hours:
            st.metric("Horas Semanales", results['weekly_hours'])
        
        # Display monthly, semester, and annual salary
        col_monthly, col_semester, col_annual = st.columns(3)
        with col_monthly:
            st.metric("Salario Mensual", f"${results['monthly_salary']:,.0f} COP")
        with col_semester:
            st.metric("Salario Semestral", f"${results['semester_salary']:,.0f} COP")
        with col_annual:
            st.metric("Salario Anual", f"${results['annual_salary']:,.0f} COP")
        
        # Show salary breakdown
        st.subheader("Desglose del Salario")
        breakdown = results["salary_breakdown"]
        
        breakdown_df = pd.DataFrame({
            "Componente": ["Tarifa por Hora", "Horas Semanales", "Base Mensual", "Tasa de Bonificación por Experiencia", 
                         "Monto de Bonificación por Experiencia", "Total Mensual", "Total Semestral", "Total Anual"],
            "Valor": [
                f"${breakdown['hourly_rate']:,.0f} COP",
                f"{breakdown['weekly_hours']} horas",
                f"${breakdown['base_monthly']:,.0f} COP",
                f"{breakdown['experience_bonus_rate']*100:.1f}%",
                f"${breakdown['experience_bonus_amount']:,.0f} COP",
                f"${breakdown['monthly_salary']:,.0f} COP",
                f"${breakdown['semester_salary']:,.0f} COP",
                f"${breakdown['annual_salary']:,.0f} COP"
            ]
        })
        
        st.table(breakdown_df)
        
        # Show salary projection
        st.subheader("Proyección Salarial")
        
        # Create and display the plot
        fig = plot_salary_evolution(
            results["salary_projection"],
            title=f"Proyección de Evolución Salarial ({base_year} - {base_year + projection_years})"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show projection table
        projection_table = pd.DataFrame({
            "Año": [p["year"] for p in results["salary_projection"]],
            "Tarifa por Hora": [f"${p['hourly_rate']:,.0f}" for p in results["salary_projection"]],
            "Salario Mensual": [f"${p['monthly_salary']:,.0f}" for p in results["salary_projection"]],
            "Salario Semestral": [f"${p['semester_salary']:,.0f}" for p in results["salary_projection"]],
            "Salario Anual": [f"${p['annual_salary']:,.0f}" for p in results["salary_projection"]]
        })
        
        st.dataframe(projection_table, use_container_width=True)
        
        # Option to simulate career evolution
        st.subheader("Simulación de Evolución de Carrera")
        simulate_evolution = st.checkbox("Simular evolución de carrera a lo largo del tiempo")
        
        if simulate_evolution:
            evolution_years = st.slider(
                "Años para simular la evolución de carrera",
                min_value=5,
                max_value=20,
                value=10
            )
            
            # Simulate career evolution
            evolution_results = acuerdo006_calculator.simulate_faculty_evolution(input_data, years=evolution_years)
            
            # Display evolution chart
            st.line_chart(
                evolution_results[["monthly_salary", "annual_salary"]].set_index(evolution_results["year"])
            )
            
            # Display evolution table
            evolution_table = pd.DataFrame({
                "Año": evolution_results["year"],
                "Experiencia": evolution_results["experience_years"],
                "Título más Alto": evolution_results["highest_degree"],
                "Tarifa por Hora": [f"${s:,.0f}" for s in evolution_results["hourly_rate"]],
                "Salario Mensual": [f"${s:,.0f}" for s in evolution_results["monthly_salary"]],
                "Salario Anual": [f"${s:,.0f}" for s in evolution_results["annual_salary"]]
            })
            
            st.dataframe(evolution_table, use_container_width=True)
    else:
        st.info("Ingrese la información del profesor y haga clic en 'Calcular Salario' para ver los resultados.")

# Explanation of Agreement 006 of 2018
st.markdown("---")
st.header("Comprensión del Acuerdo 006 de 2018")

st.markdown("""
### Componentes Clave del Acuerdo 006 de 2018

El Acuerdo 006 de 2018 regula la contratación y el pago de profesores ocasionales en la UPC (Universidad Piloto de Colombia). Los principales componentes que determinan el salario de un profesor ocasional son:

1. **Títulos Académicos**: La tarifa por hora se determina según el título académico más alto:
   - Pregrado: Tarifa base
   - Especialización: Tarifa más alta
   - Maestría: Tarifa aún más alta
   - Doctorado: Tarifa máxima

2. **Tipo de Dedicación**: Existen tres tipos de dedicación:
   - Tiempo Completo: 40 horas por semana
   - Medio Tiempo: 20 horas por semana
   - Hora Cátedra: Horas variables por semana (hasta 19)

3. **Experiencia**: Porcentaje adicional aplicado según los años de experiencia:
   - 0-2 años: Sin porcentaje adicional
   - 3-5 años: 5% adicional
   - 6-10 años: 10% adicional
   - 11+ años: 15% adicional

### Cálculo del Salario

El salario se calcula:
1. Determinando la tarifa por hora según la titulación académica
2. Multiplicando por las horas semanales
3. Multiplicando por 4 semanas para obtener el salario mensual
4. Agregando la bonificación por experiencia
5. Para el salario semestral, multiplicando la tarifa por hora por las horas semanales y el número de semanas en un semestre (16)
6. Para el salario anual, multiplicando el salario semestral por 2 (asumiendo dos semestres por año)

Esta calculadora implementa estos cálculos de acuerdo con las especificaciones del Acuerdo.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Simulador de Salarios Docentes UPC - Módulo Acuerdo 006")
