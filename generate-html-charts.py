import altair as alt
import pandas as pd
from covid import dataimport
from covid import chart

fhm_data, labels = dataimport.get_fhm_data()
df = fhm_data[fhm_data['date'] >= '2020-03-13']

chart = chart.lag_chart_with_selection(df, labels)
chart.save('charts/filter-publication-date.html')