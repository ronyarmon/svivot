#!/usr/bin/env python
# coding: utf-8

# # Data Science Jobs Dashboard
# source: https://towardsdatascience.com/using-panel-to-build-data-dashboards-in-python-e87a04c9034d  
# dataset: https://www.kaggle.com/code/sumon9300/data-science-job-salaries/input

import os, getpass
import pandas as pd
import holoviews as hv
import hvplot.pandas
import panel as pn
from pylab import *
from bokeh.resources import INLINE
hv.extension('bokeh')
pn.extension()

## Data
data_dir = os.path.join('/home', getpass.getuser(), 'data')
# Jobs
jobs = pd.read_csv(os.path.join(data_dir, 'ds_salaries.csv'), index_col=0)
jobs['experience_level'] = jobs['experience_level'].map({'SE':'Senior', 'MI':'Intermediate','EN':'Junior', 'EX':'Executive'})
jobs['employment_type'] = jobs['employment_type'].map({'PT':'Part-time','FT': 'Full-time', 'CT': 'Contract','FL':'Freelance'})
jobs['company_size'] = jobs['company_size'].map({'M': 'Medium', 'L': 'Large', 'S':'Small'})
jobs.drop(['salary', 'salary_currency'], axis=1, inplace=True)

# Country locations
# Unique Countries
countries = list(set(jobs['company_location']) | set(jobs['employee_residence']))
locationsDf = pd.DataFrame(countries, columns = ["Countries"])
cmap = cm.get_cmap('Spectral', 59)
colors = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]
locationsDf["colors"] = colors

# Year Slider
pn.extension(sizing_mode='fixed')
year = pn.widgets.IntSlider(name='Year Slider', width=200,
                                 start=2020, end=2022, value=(2020),
                                 step=1,value_throttled=(2020))
@pn.depends(year.param.value_throttled)
def year_selected(year):
    return '### Jobs in {}'.format(year)

# Plots
country_colors_dict = dict(zip(locationsDf['Countries'], locationsDf['colors']))

def plot_bars1(year):
    year_df = jobs[jobs['work_year'] == year]
    return year_df.hvplot.bar('experience_level', 'salary_in_usd', c='experience_level',
                       cmap=colors, height=350, width=600, legend=False,
                       yformatter='%.0f').aggregate(function=np.mean).opts(xlabel="Experience Level",
                                               ylabel="Avg Salary (USD)",
                                               title="Average Salary by Experience Level in 2021")

@pn.depends(year.param.value_throttled)
def plot_bars2(year):
    year_df = jobs[jobs['work_year'] == year]
    df = pd.DataFrame(year_df.groupby('employee_residence')[['salary_in_usd']]
                      .mean().sort_values('salary_in_usd', ascending=False).round(2).head(10))
    df['employee_residence'] = df.index
    return df.hvplot.bar(x='employee_residence', y='salary_in_usd',c='employee_residence',
                         cmap=country_colors_dict, min_height=250, min_width=400, legend=False, yformatter='%.0f', 
                         responsive=True).opts(xlabel="Employee Residence", ylabel="Avg Salary (USD)")

@pn.depends(year.param.value_throttled)
def plot_bars3(year):
        """Plot salary based on company location and subset by the year"""
        year_df = jobs[jobs['work_year'] == year]
        df = pd.DataFrame(year_df.groupby('company_location')[['salary_in_usd']]
                          .mean().sort_values('salary_in_usd', ascending=False).round(3).head(10))
        df['company_location'] = df.index
        return df.hvplot.bar(x='company_location', y='salary_in_usd',
                             c='company_location', cmap=country_colors_dict, 
                             min_height=250, min_width=400, legend=False, yformatter='%.0f', 
                             responsive=True).opts(xlabel="Company Location", ylabel="Avg Salary (USD)")

@pn.depends(year.param.value_throttled)
def plot_bars4(year):
    year_df = jobs[jobs['work_year'] == year]
    df = pd.DataFrame(year_df.groupby('company_size')[['salary_in_usd']]
                          .mean().sort_values('salary_in_usd', ascending=False).round(3).head(10))
    df['company_size'] = df.index
    colors_dict = dict(zip(df['company_size'], hv.Cycle('Category10').values))
    return  df.hvplot.bar(x='company_size', y='salary_in_usd',
                          c='company_size', cmap=colors_dict, 
                          min_height=250, min_width=400, legend=False, yformatter='%.0f', 
                          responsive=True).opts(xlabel="Company Size", ylabel="Avg Salary (USD)")

colors = {
    'Intermediate': '#1f77b4',
    'Senior': '#ff7f0e',
    'Junior': '#2ca02c',
    'Executive': '#324d67'
}

@pn.depends(year.param.value_throttled)
def plot_bars1(year):
    year_df = jobs[jobs['work_year'] == year]
    return year_df.hvplot.bar('experience_level', 'salary_in_usd', c='experience_level',
                       cmap=colors, responsive=True, min_height=250, min_width=400, legend=False,
                       yformatter='%.0f').aggregate(function=np.mean).opts(xlabel="Experience Level",
                                                                           ylabel="Avg Salary (USD)")
# Dashboard
plots_box = pn.WidgetBox(pn.Column(pn.Row(year_selected, year),
				   pn.Row(pn.bind(plot_bars1, year), pn.bind(plot_bars4,year)), pn.Row(pn.bind(plot_bars2,year), 
                                   pn.bind(plot_bars3,year)), align="start",
                                   sizing_mode="stretch_width"))
dashboard = pn.Row(plots_box, sizing_mode="stretch_width")
dashboard.save('results/ds_salaries_dashboard.html', resources=INLINE)
dashboard.servable()