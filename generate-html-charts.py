import altair as alt
import pandas as pd
from coviddata.fhm import get_fhm_data
from covidchart.lag import lag_chart_with_selection

fhm_data, labels = get_fhm_data()
df = fhm_data[fhm_data['date'] >= '2020-03-13']

chart = lag_chart_with_selection(df, labels)
chart.save('charts/filter-publication-date.html')