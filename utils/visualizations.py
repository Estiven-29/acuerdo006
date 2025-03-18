import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_salary_evolution(salary_projection, title="Occasional Faculty Salary Evolution"):
    df = pd.DataFrame(salary_projection)
    
    # Create figure
    fig = px.line(
        df, 
        x="year", 
        y=["monthly_salary", "monthly_with_bonus"] if "monthly_with_bonus" in df.columns else "monthly_salary",
        title=title,
        labels={"value": "Salary (COP)", "year": "Year", "variable": "Type"}
    )
    
    # Update layout
    fig.update_layout(
        hovermode="x unified",
        legend_title="Salary Component",
        template="plotly_white"
    )
    
    return fig

def plot_ocasional_payroll_projection(ocasional_projections):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Total Occasional Faculty Payroll Projection", "Percentage by Dedication Type"),
        specs=[[{"type": "scatter"}], [{"type": "bar"}]],
        row_heights=[0.6, 0.4],
        vertical_spacing=0.1
    )
    
    # Add traces for total payroll
    fig.add_trace(
        go.Scatter(
            x=ocasional_projections["year"], 
            y=ocasional_projections["total_ocasional"],
            mode="lines+markers",
            name="Total Occasional",
            line=dict(color="green", width=4),
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    
    # Add traces for dedication types (assuming they exist in the data)
    if "total_tiempo_completo" in ocasional_projections.columns:
        fig.add_trace(
            go.Scatter(
                x=ocasional_projections["year"], 
                y=ocasional_projections["total_tiempo_completo"],
                mode="lines+markers",
                name="Tiempo Completo",
                line=dict(color="darkgreen", width=2, dash="dash"),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
    
    if "total_medio_tiempo" in ocasional_projections.columns:
        fig.add_trace(
            go.Scatter(
                x=ocasional_projections["year"], 
                y=ocasional_projections["total_medio_tiempo"],
                mode="lines+markers",
                name="Medio Tiempo",
                line=dict(color="olive", width=2, dash="dash"),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
    
    if "total_hora_catedra" in ocasional_projections.columns:
        fig.add_trace(
            go.Scatter(
                x=ocasional_projections["year"], 
                y=ocasional_projections["total_hora_catedra"],
                mode="lines+markers",
                name="Hora Cátedra",
                line=dict(color="lightgreen", width=2, dash="dash"),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
    
    # Add traces for percentage breakdown
    if "tiempo_completo_percentage" in ocasional_projections.columns:
        fig.add_trace(
            go.Bar(
                x=ocasional_projections["year"], 
                y=ocasional_projections["tiempo_completo_percentage"],
                name="Tiempo Completo %",
                marker_color="darkgreen"
            ),
            row=2, col=1
        )
    
    if "medio_tiempo_percentage" in ocasional_projections.columns:
        fig.add_trace(
            go.Bar(
                x=ocasional_projections["year"], 
                y=ocasional_projections["medio_tiempo_percentage"],
                name="Medio Tiempo %",
                marker_color="olive"
            ),
            row=2, col=1
        )
    
    if "hora_catedra_percentage" in ocasional_projections.columns:
        fig.add_trace(
            go.Bar(
                x=ocasional_projections["year"], 
                y=ocasional_projections["hora_catedra_percentage"],
                name="Hora Cátedra %",
                marker_color="lightgreen"
            ),
            row=2, col=1
        )
    
    # Update layout
    fig.update_layout(
        title="Occasional Faculty Payroll Projection Over Time",
        height=800,
        barmode="stack",
        hovermode="x unified",
        template="plotly_white"
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Annual Cost (COP)", row=1, col=1)
    fig.update_yaxes(title_text="Percentage (%)", row=2, col=1)
    
    # Update x-axes
    fig.update_xaxes(title_text="Year", row=2, col=1)
    
    return fig

def plot_ocasional_faculty_distribution(ocasional_data):
    ocasional_df = ocasional_data["ocasional_salaries"]
    
    ocasional_dedication_fig = px.pie(
        ocasional_df, 
        names="dedication_type",
        title="Occasional Faculty by Dedication Type",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    ocasional_degree_fig = px.pie(
        ocasional_df, 
        names="highest_degree",
        title="Occasional Faculty by Highest Degree",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Update layouts
    for fig in [ocasional_dedication_fig, ocasional_degree_fig]:
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            uniformtext_minsize=12, 
            uniformtext_mode='hide',
            template="plotly_white"
        )
    
    return ocasional_dedication_fig, ocasional_degree_fig

def plot_ocasional_salary_distribution(ocasional_data):
    ocasional_df = ocasional_data["ocasional_salaries"]
    
    # Create histogram for occasional faculty salaries
    ocasional_hist = px.histogram(
        ocasional_df,
        x="monthly_salary",
        title="Distribution of Occasional Faculty Salaries",
        labels={"monthly_salary": "Monthly Salary (COP)"},
        marginal="box",
        color="dedication_type",
        nbins=20
    )
    
    # Update layout
    ocasional_hist.update_layout(
        barmode="overlay",
        template="plotly_white"
    )
    
    # Create box plot by dedication type and degree
    ocasional_box = px.box(
        ocasional_df,
        x="dedication_type",
        y="monthly_salary",
        color="highest_degree",
        title="Occasional Faculty Salary by Dedication and Degree",
        labels={"monthly_salary": "Monthly Salary (COP)", "dedication_type": "Dedication Type"}
    )
    
    # Update layout
    ocasional_box.update_layout(template="plotly_white")
    
    return ocasional_hist, ocasional_box

def plot_ocasional_payroll_breakdown(ocasional_data):
    stats = ocasional_data["payroll_stats"]
    
    # Create data for the sunburst chart
    sunburst_data = [
        # Level 1: Total Payroll
        {"id": "Total Occasional", "parent": "", "value": stats["ocasional"]["total_annual"]},
        
        # Level 2: Dedication Types
        {"id": "Tiempo Completo", "parent": "Total Occasional", 
         "value": stats["ocasional"]["total_annual"] * 0.6},  # Approximate
        {"id": "Medio Tiempo", "parent": "Total Occasional", 
         "value": stats["ocasional"]["total_annual"] * 0.25},  # Approximate
        {"id": "Hora Cátedra", "parent": "Total Occasional", 
         "value": stats["ocasional"]["total_annual"] * 0.15}   # Approximate
    ]
    
    # Add degree breakdown for each dedication type if available
    if "highest_degree_breakdown" in stats["ocasional"]:
        degree_breakdown = stats["ocasional"]["highest_degree_breakdown"]
        for degree, percentage in degree_breakdown.items():
            for dedication in ["Tiempo Completo", "Medio Tiempo", "Hora Cátedra"]:
                # Use estimated percentages for different dedication types
                ded_percentage = 0.6 if dedication == "Tiempo Completo" else (0.25 if dedication == "Medio Tiempo" else 0.15)
                value = stats["ocasional"]["total_annual"] * ded_percentage * percentage
                sunburst_data.append({
                    "id": f"{dedication} - {degree}",
                    "parent": dedication,
                    "value": value
                })
    
    # Create DataFrame
    sunburst_df = pd.DataFrame(sunburst_data)
    
    # Create sunburst chart
    fig = px.sunburst(
        sunburst_df,
        ids="id",
        parents="parent",
        values="value",
        title="Occasional Faculty Payroll Breakdown",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    # Update layout
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=60, l=0, r=0, b=0)
    )
    
    return fig