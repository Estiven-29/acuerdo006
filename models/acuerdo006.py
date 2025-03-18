import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Acuerdo006Calculator:
    
    def __init__(self):
        self.hourly_rates = {
            "Pregrado": 28000,
            "Especialización": 32000,
            "Maestría": 38000,
            "Doctorado": 48000
        }
        
        self.dedication_types = {
            "Tiempo Completo": 40,
            "Medio Tiempo": 20,
            "Hora Cátedra": None
        }
        
        self.experience_bonus = {
            "0-2 años": 0.00,
            "3-5 años": 0.05,
            "6-10 años": 0.10,
            "11+ años": 0.15
        }
        
        self.weeks_per_semester = 16
    
    def calculate_salary(self, input_data):

        highest_degree = input_data.get('highest_degree', 'Pregrado')
        dedication_type = input_data.get('dedication_type', 'Tiempo Completo')
        experience_years = input_data.get('experience_years', 0)
        base_year = input_data.get('base_year', 2024)
        projection_years = input_data.get('projection_years', 5)
        
        hourly_rate = self.hourly_rates.get(highest_degree, self.hourly_rates['Pregrado'])
        
        if dedication_type == "Hora Cátedra":
            weekly_hours = input_data.get('weekly_hours', 8)
        else:
            weekly_hours = self.dedication_types.get(dedication_type, 40)
        
        # Calculate experience bonus
        if experience_years <= 2:
            experience_category = "0-2 años"
        elif experience_years <= 5:
            experience_category = "3-5 años"
        elif experience_years <= 10:
            experience_category = "6-10 años"
        else:
            experience_category = "11+ años"
            
        experience_bonus_rate = self.experience_bonus.get(experience_category, 0)
        
        # Calculate mes salario
        base_monthly = hourly_rate * weekly_hours * 4
        experience_bonus_amount = base_monthly * experience_bonus_rate
        monthly_salary = base_monthly + experience_bonus_amount
        
        # Calculate semestral y anual salario
        semester_salary = hourly_rate * weekly_hours * self.weeks_per_semester
        annual_salary = semester_salary * 2
        
        salary_breakdown = {
            'hourly_rate': hourly_rate,
            'weekly_hours': weekly_hours,
            'base_monthly': base_monthly,
            'experience_bonus_rate': experience_bonus_rate,
            'experience_bonus_amount': experience_bonus_amount,
            'monthly_salary': monthly_salary,
            'semester_salary': semester_salary,
            'annual_salary': annual_salary
        }
        
        
        inflation_rate = 0.04
        projection = []
        
        for i in range(projection_years + 1):
            year = base_year + i
            projected_hourly_rate = hourly_rate * ((1 + inflation_rate) ** i)
            projected_base_monthly = projected_hourly_rate * weekly_hours * 4
            projected_bonus = projected_base_monthly * experience_bonus_rate
            projected_monthly = projected_base_monthly + projected_bonus
            projected_semester = projected_hourly_rate * weekly_hours * self.weeks_per_semester
            projected_annual = projected_semester * 2
            
            projection.append({
                'year': year,
                'hourly_rate': projected_hourly_rate,
                'monthly_salary': projected_monthly,
                'semester_salary': projected_semester,
                'annual_salary': projected_annual
            })
        
        return {
            'hourly_rate': hourly_rate,
            'weekly_hours': weekly_hours,
            'monthly_salary': monthly_salary,
            'semester_salary': semester_salary,
            'annual_salary': annual_salary,
            'salary_breakdown': salary_breakdown,
            'salary_projection': projection
        }
    
    def simulate_faculty_evolution(self, faculty_data, years=10):
        results = []
        current_data = faculty_data.copy()
        
        for year in range(years):
            current_data['experience_years'] = faculty_data['experience_years'] + year
            
            if year == 2 and current_data['highest_degree'] == 'Pregrado':
                current_data['highest_degree'] = 'Especialización'
            elif year == 4 and current_data['highest_degree'] == 'Especialización':
                current_data['highest_degree'] = 'Maestría'
            current_data['base_year'] = faculty_data['base_year'] + year
            calculation = self.calculate_salary(current_data)
            
            results.append({
                'year': faculty_data['base_year'] + year,
                'experience_years': current_data['experience_years'],
                'highest_degree': current_data['highest_degree'],
                'dedication_type': current_data['dedication_type'],
                'hourly_rate': calculation['hourly_rate'],
                'monthly_salary': calculation['monthly_salary'],
                'annual_salary': calculation['annual_salary']
            })
        
        return pd.DataFrame(results)
