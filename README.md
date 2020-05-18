# Python notebooks for Covid-19 data
Notebooks for analysing some Covid-19 data from different sources. Feel free to use the issue tracker for feedback and general discussion.

## Reporting Lag
Using data published by FHM and [processed by @adamaltmejd](https://github.com/adamaltmejd/covid).

[![](images/example.gif)](https://morberg.github.io/covid-notebook/charts/filter-publication-date.html)
[Interactive graph of daily deaths](https://morberg.github.io/covid-notebook/charts/filter-publication-date.html). Click and drag in bottom graph to select a time period for reported deaths to show in the upper graph.

[![](images/lag-chart.png)](https://morberg.github.io/covid-notebook/charts/lag-chart.html)

Average lag by reporting date. Line size is number of deaths reported each day.

Some other graphs are available in the notebook. You can work with it live on [Google Colab](https://colab.research.google.com/github/morberg/covid-notebook/blob/master/covid-lag-sweden.ipynb).

## Total Death Count
Based on data from Statistiska Centralbyrån. Interactive version on [Google Colab](https://colab.research.google.com/github/morberg/covid-notebook/blob/master/county-data.ipynb)

You can view an [interactive graph of weekly deaths](https://morberg.github.io/covid-notebook/charts/weekly-deaths.html) in your browser. Click a county in the legend or in the bottom graph to show only that county. Shift-click to multi-select. Click and drag in main graph to select a time period.

### Total for Sweden
Death count for 2018-2020. The lines are 20 day rolling averages.
![](images/daily-deaths-total.png?raw=true)

### Total by subset of counties
This graph shows daily death count for four counties. Deaths from 2018-2019 are shown as opaque points, 2020 as a line graph. If you [run the notebook](https://colab.research.google.com/github/morberg/covid-notebook/blob/master/county-data.ipynb) you can interactively select the counties you want.
![](images/daily-deaths-by-county.png?raw=true)
