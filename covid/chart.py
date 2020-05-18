import pandas as pd
import altair as alt

def lag_chart_with_selection(df, labels):
    """
    Generate chart showing lag in reporting with interactive filter on reported date

    Input
    -----
    df : pandas.DataFrame
        Typically generated from get_fhm_data() in coviddata package
    labels : array
        Labels for column 'lag' in data. Returned from get_fhm_data()

    Returns
    -------
    chart : alt.Chart
    """

    # Dates to display on the x-axis
    domain = [df.date.min().date().isoformat(), (df.date.max() + pd.Timedelta('1D')).date().isoformat()]

    brush = alt.selection(type='interval', encodings=['x'])

    deceased = alt.Chart(df, height=400, width=800).mark_bar().encode(
        x=alt.X('yearmonthdate(date)', title='Date Deceased', scale=alt.Scale(domain=domain)),
        y=alt.Y('sum(n_diff)', title='Deceased', scale=alt.Scale(domain=[0, df.N.max()])),
        order=alt.Order(
        # Sort the segments of the bars by this field
        'days_since_publication',
        sort='ascending'
        ),
        color=alt.Color(
            'lag:O',
            title='Lag in Days',
            sort=labels,
            scale=alt.Scale(scheme='category20c'),
        )
    ).transform_filter(
        brush
    )

    reported = alt.Chart(df, height=100, width=800).mark_bar().encode(
        x=alt.X('yearmonthdate(publication_date)', title='Publication Date', scale=alt.Scale(domain=domain)),
        y=alt.Y('sum(n_diff)', title='Reported Deaths')
    ).add_selection(brush)

    legend_vert = alt.Chart(df, width=80, title='Reporting Lag in Days').mark_bar().encode(
        x=alt.X('sum(n_diff)', title='Reported Deaths'),
        y=alt.Y('lag', title='', sort=labels),
        color=alt.Color(
            'lag:O',
            sort=labels,
            legend=None
        )
    ).transform_filter(
        brush
    )

    text = alt.Chart(df).transform_filter(
        brush
    ).transform_aggregate(
        sum_deaths='sum(n_diff)'
    ).transform_calculate(
        text="Total deaths: " + alt.datum.sum_deaths
    ).mark_text(
        align='right',
        x=792,
        y=19, 
        fontSize=18
    ).encode(text='text:N')

    chart = deceased + text & reported | legend_vert
    return chart
