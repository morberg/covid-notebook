import altair as alt
import pandas as pd
from covid import dataimport
from covid import chart

fhm_data, labels = dataimport.get_fhm_data()

df = fhm_data[fhm_data['date'] >= '2020-03-13']
chart.lag_chart_with_selection(df, labels).save(
    'charts/filter-publication-date.html')

chart.average_lag(fhm_data, '2020-04-03').save(
    'charts/lag-chart.html')

df = fhm_data.dropna(subset=['days_since_publication'])
df = df[df.date >= '2020-04-06'] # Start on first relevant Monday
chart.daily_reported_deaths(df, labels).save(
    'charts/daily-reported-deaths.html')