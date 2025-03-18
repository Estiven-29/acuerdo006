import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_salary_evolution(input_data):
    # Extract input parameters
    initial_year = input_data["initial_year"]
    years_to_simulate = input_data["years_to_simulate"]
    annual_articles = input_data["annual_articles"]
    annual_books = input_data["annual_books"]
    initial_point_value = input_data["initial_point_value"]
    annual_point_increase_pct = input_data["annual_point_increase_pct"] / 100
    inflation_adjusted = input_data["inflation_adjusted"]
    annual_inflation = input_data["annual_inflation"] / 100 if inflation_adjusted else 0
    
    # Initialize results
    years = list(range(initial_year, initial_year + years_to_simulate + 1))
    salaries = []
    real_salaries = []
    point_values = []
    education_levels = []
    career_events = []
    cumulative_earnings = [0]
    
    # Track professor attributes
    current_year = initial_year
    total_articles = 0
    total_books = 0
    
    # Initial education level
    education_level = input_data["education_level"]
    contract_type = input_data["contract_type"]
    
    # Future education levels
    future_education = {}
    for i, edu in enumerate(input_data["education_path"]):
        achievement_year = initial_year + np.random.randint(1, min(10, years_to_simulate))
        future_education[achievement_year] = edu
    
    # Simulate year by year
    for year_idx, year in enumerate(years):
        # Update point value for the year (though not used directly for occasional professors)
        point_value = initial_point_value * (1 + annual_point_increase_pct) ** year_idx
        point_values.append(point_value)
        
        # Check for education level changes this year
        if year in future_education:
            education_level = future_education[year]
            event_description = f"Completed {education_level}"
            
            # Record career event
            career_events.append({
                "Year": year,
                "Event": event_description,
                "Event Type": "Education",
                "Impact": 10  # Impact size for visualization
            })
        
        # Increment articles and books (rounded to nearest whole number)
        if year_idx > 0:  # Skip the first year
            new_articles = np.random.poisson(annual_articles)
            new_books = 1 if np.random.random() < annual_books else 0
            
            total_articles += new_articles
            total_books += new_books
            
            # Record significant publication events
            if new_articles >= 3:
                career_events.append({
                    "Year": year,
                    "Event": f"Published {new_articles} research articles",
                    "Event Type": "Publication",
                    "Impact": 8
                })
            
            if new_books > 0:
                career_events.append({
                    "Year": year,
                    "Event": f"Published {new_books} book(s)",
                    "Event Type": "Publication",
                    "Impact": 12
                })
        
        # Calculate salary for the year
        years_experience = year_idx  # Years since initial year
        contract_months = 11  # Assuming almost full year for simplicity
        has_research = np.random.random() < 0.4
        has_extension = np.random.random() < 0.3
        
        input_data_salary = {
            "education_level": education_level,
            "contract_type": contract_type,
            "contract_months": contract_months,
            "years_experience": years_experience,
            "teaching_hours": 20 if contract_type == "Full-Time" else 10,
            "has_research": has_research,
            "has_extension": has_extension
        }
        
        from models.acuerdo006 import calculate_occasional_salary
        salary_result = calculate_occasional_salary(input_data_salary)
        
        # For occasional professors, use the monthly salary and extrapolate to a year
        annual_salary = salary_result["monthly_salary"] * 12
        
        # Apply inflation adjustment if requested
        if inflation_adjusted:
            real_value = annual_salary / ((1 + annual_inflation) ** year_idx)
            real_salaries.append(real_value)
        
        # Add to cumulative earnings
        if year_idx > 0:  # Skip the initial year
            cumulative_earnings.append(cumulative_earnings[-1] + annual_salary)
        
        # Store results
        salaries.append(annual_salary)
        education_levels.append(education_level)
    
    # Create dataframe with evolution data
    evolution_data = pd.DataFrame({
        "Year": years,
        "Annual Salary": salaries,
        "Education Level": education_levels,
        "Point Value": [None] * len(years),  # Not applicable for occasional professors
        "Cumulative Earnings": cumulative_earnings
    })
    
    if inflation_adjusted:
        evolution_data["Real Salary (Inflation-Adjusted)"] = real_salaries
    
    # Create salary evolution chart
    fig = go.Figure()
    
    # Nominal salary
    fig.add_trace(go.Scatter(
        x=years, 
        y=salaries,
        mode='lines+markers',
        name='Nominal Salary',
        line=dict(color='royalblue', width=3)
    ))
    
    # Real salary (if applicable)
    if inflation_adjusted:
        fig.add_trace(go.Scatter(
            x=years, 
            y=real_salaries,
            mode='lines+markers',
            name='Real Salary (Inflation-Adjusted)',
            line=dict(color='firebrick', width=3, dash='dash')
        ))
    
    # Add career events as markers
    if career_events:
        events_df = pd.DataFrame(career_events)
        
        for event_type in events_df["Event Type"].unique():
            type_events = events_df[events_df["Event Type"] == event_type]
            
            # Get salary values for these years
            event_salaries = []
            for year in type_events["Year"]:
                year_idx = years.index(year)
                event_salaries.append(salaries[year_idx])
            
            # Add to plot
            fig.add_trace(go.Scatter(
                x=type_events["Year"],
                y=event_salaries,
                mode='markers',
                marker=dict(
                    size=type_events["Impact"] * 2,
                    symbol='star',
                    line=dict(width=2, color='DarkSlateGrey')
                ),
                name=event_type,
                text=type_events["Event"],
                hoverinfo='text+x+y'
            ))
    
    # Update layout
    fig.update_layout(
        title=f'Salary Evolution for Occasional Professor (2025-{initial_year + years_to_simulate})',
        xaxis_title='Year',
        yaxis_title='Annual Salary (COP)',
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Create cumulative earnings chart
    cumulative_fig = go.Figure(go.Scatter(
        x=years, 
        y=cumulative_earnings,
        mode='lines+markers',
        name='Cumulative Earnings',
        fill='tozeroy',
        line=dict(color='green', width=3)
    ))
    
    cumulative_fig.update_layout(
        title='Cumulative Earnings Over Career',
        xaxis_title='Year',
        yaxis_title='Cumulative Earnings (COP)',
        hovermode='closest'
    )
    
    return {
        "salary_chart": fig,
        "cumulative_chart": cumulative_fig,
        "evolution_data": evolution_data,
        "career_events": pd.DataFrame(career_events) if career_events else pd.DataFrame(),
        "initial_salary": salaries[0],
        "final_salary": salaries[-1],
        "total_earnings": cumulative_earnings[-1]
    }

def plot_payroll_distribution(payroll_data):
    return {}