"""
Script to play around with bokeh using the Our World In Data COVID-19 dataset (https://ourworldindata.org/coronavirus)

Date: 2021-03-12
"""

import pandas as pd
import wget
import os
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Spectral6, Colorblind6
from bokeh.transform import factor_cmap
from bokeh.layouts import column

def testBarPlot():
    """
    Test bar plot
    """
    countries = ["Hungary", "Austria", "Slovakia", "Czechia"]
    counts = [5, 3, 4, 2]
    source = ColumnDataSource(data=dict(countries=countries, counts=counts))
    color_cmap = factor_cmap("countries", palette=Spectral6, factors=countries)

    plot = figure(plot_height=720, plot_width=1280, x_range=countries, x_axis_label="Country", y_axis_label="Count")
    plot.vbar(x="countries", top="counts", width=1, source=source, legend_field="countries", line_color="white", fill_color=color_cmap)
    plot.legend.location = "top_center"
    plot.legend.orientation = "horizontal"
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0
    plot.y_range.end = 9

    show(plot)

def downloadData():
    """
    Download owid-covid-data.csv
    """
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

    try:
        result = wget.download(url, "")
    except Exception as e:
        result = 0

    if result != 0:
        os.remove(os.path.basename(url))
        os.rename(result, "owid-covid-data.csv")

def loadData():
    """
    Loads data from the csv, sets index and drops unused columns
    """
    df = pd.read_csv("owid-covid-data.csv", sep=",", parse_dates=["date"], na_values=[""])
    df.set_index("date", inplace=True)

    df.drop(["iso_code", "continent", "total_cases", "new_cases_smoothed", "new_deaths_smoothed", "total_cases_per_million", "new_cases_per_million", "new_cases_smoothed_per_million", "total_deaths_per_million", "new_deaths_per_million", "new_deaths_smoothed_per_million", "reproduction_rate", "icu_patients_per_million", "hosp_patients_per_million", "weekly_icu_admissions", "weekly_icu_admissions_per_million", "weekly_hosp_admissions", "weekly_hosp_admissions_per_million", "total_tests", "total_tests_per_thousand", "new_tests_per_thousand", "new_tests_smoothed", "new_tests_smoothed_per_thousand", "positive_rate", "tests_per_case", "tests_units", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "new_vaccinations_smoothed", "total_vaccinations_per_hundred", "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred", "new_vaccinations_smoothed_per_million", "stringency_index", "population", "population_density", "median_age", "aged_65_older", "aged_70_older", "gdp_per_capita", "extreme_poverty", "cardiovasc_death_rate", "diabetes_prevalence", "female_smokers", "male_smokers", "handwashing_facilities", "hospital_beds_per_thousand", "life_expectancy", "human_development_index"], axis=1, inplace=True)

    return df

def linePlotDeathsByCountries(df, countries):
    """
    Prints the countries new deaths for every day
    TODO: the colormapper not working for some reason. Cannot print each line with a different color.
    """
    data = df[df["location"].isin(countries)]
    source = ColumnDataSource(data=data)
    color_cmap = factor_cmap("location", palette=Colorblind6, factors=countries)

    hover_tooltip = HoverTool(tooltips=[("country", "@location"), ("new deaths", "@new_deaths"), ("date", "@date{%Y. %m. %d.}")], formatters={'@date': 'datetime'},)

    plot = figure(plot_height=720, plot_width=1280, x_axis_type="datetime", x_axis_label="Date", y_axis_label="New deaths", tools=[hover_tooltip, "pan", "wheel_zoom", "reset"])
    plot.line("date", "new_deaths", source=source, width=2, line_color=color_cmap, legend_field="location")
    plot.legend.location = "top_left"

    return plot

def barPlotCases(df, country):
    """
    A bar plot that prints out the new cases for every day for a country.
    """
    data = df[df["location"] == country]
    source = ColumnDataSource(data=data)

    hover_tooltip = HoverTool(tooltips=[("country", "@location"), ("new cases", "@new_cases"), ("date", "@date{%Y. %m. %d.}")], formatters={'@date': 'datetime'},)

    plot = figure(plot_height=720, plot_width=1280, x_axis_type="datetime", tools=[hover_tooltip, "pan", "box_zoom", "wheel_zoom", "reset"])
    plot.vbar(x="date", top="new_cases", width=80000000, source=source, line_color="white", fill_color="orange")
    plot.xgrid.grid_line_color = None
    plot.title = country + " - New Cases per Day"

    return plot

def barPlotCasesByCountries(df, countries):
    """
    A bar plot that prints out the new cases for every day for a country.
    TODO: colors are too similar
    """
    data = df[df["location"].isin(countries)]
    source = ColumnDataSource(data=data)
    color_cmap = factor_cmap("location", palette=Colorblind6, factors=countries)

    hover_tooltip = HoverTool(tooltips=[("country", "@location"), ("new cases", "@new_cases"), ("date", "@date{%Y. %m. %d.}")], formatters={'@date': 'datetime'},)

    plot = figure(title="New Cases per Day by Countries", plot_height=720, plot_width=1280, x_axis_type="datetime", tools=[hover_tooltip, "pan", "box_zoom", "wheel_zoom", "reset"])
    plot.vbar(x="date", top="new_cases", width=80000000, source=source, line_color="white", fill_color=color_cmap, legend_field="location")
    plot.legend.location = "top_center"
    plot.legend.orientation = "horizontal"
    plot.xgrid.grid_line_color = None

    return plot

def barPlotDeaths(df, country):
    """
    A bar plot that prints out the new deaths for every day for a country.
    """
    data = df[df["location"] == country]
    source = ColumnDataSource(data=data)

    hover_tooltip = HoverTool(tooltips=[("country", "@location"), ("new deaths", "@new_deaths"), ("date", "@date{%Y. %m. %d.}")], formatters={'@date': 'datetime'},)

    plot = figure(plot_height=720, plot_width=1280, x_axis_type="datetime", tools=[hover_tooltip, "pan", "box_zoom", "wheel_zoom", "reset"])
    plot.vbar(x="date", top="new_deaths", width=80000000, source=source, line_color="white", fill_color="red")
    plot.xgrid.grid_line_color = None
    plot.title = country + " - New Deaths per Day"

    return plot

def barPlotTotalDeathsByCountries(df, countries, date):
    """
    Bar plot that prints out the total deaths for selected countries for a selected day.
    Using colormapper to plot every country with a different color.
    """
    data = df[df["location"].isin(countries)]
    data = data.loc[date]

    source = ColumnDataSource(data=data)
    color_cmap = factor_cmap("location", palette=Spectral6, factors=countries)

    hover_tooltip = HoverTool(tooltips=[("country", "@location"), ("total deaths", "@total_deaths")],)

    plot = figure(title="Total Deathy by Countries", plot_height=720, plot_width=1280, x_range=countries, tools=[hover_tooltip, "pan", "box_zoom", "wheel_zoom", "reset"])
    plot.vbar(x="location", top="total_deaths", width=0.9, source=source, line_color="white", fill_color=color_cmap, legend_field="location")
    plot.legend.location = "top_center"
    plot.legend.orientation = "horizontal"
    plot.xgrid.grid_line_color = None

    return plot

def run():

    #downloadData()
    data = loadData()
    countries = ["Hungary", "Austria", "Slovakia", "Czechia"]

    #testBarPlot()
    #linePlotDeathsByCountries(data, countries)
    plot1 = barPlotCasesByCountries(data, countries)
    plot2 = barPlotCases(data, "Hungary")
    plot3 = barPlotCases(data, "Austria")
    plot4 = barPlotDeaths(data, "Hungary")
    plot5 = barPlotDeaths(data, "Austria")
    plot6 = barPlotTotalDeathsByCountries(data, countries, "2021-03-11")

    show(column(plot1, plot2, plot3, plot4, plot5, plot6))

if __name__ == "__main__":
    run()
