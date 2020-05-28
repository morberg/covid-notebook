import pandas as pd
import altair as alt


def lag_chart_with_selection(df, labels):
    """
    Generate chart showing lag in reporting with interactive filter on reported date

    Input
    -----
    df : pandas.DataFrame
        Typically generated from get_lag_data() in coviddata package
    labels : array
        Labels for column 'lag' in data. Returned from get_lag_data()

    Returns
    -------
    chart : alt.Chart
    """

    # Dates to display on the x-axis
    domain = [
        df.date.min().date().isoformat(),
        (df.date.max() + pd.Timedelta("1D")).date().isoformat(),
    ]

    brush = alt.selection(type="interval", encodings=["x"])

    deceased = (
        alt.Chart(df, height=400, width=800)
        .mark_bar()
        .encode(
            x=alt.X(
                "yearmonthdate(date)",
                title="Date Deceased",
                scale=alt.Scale(domain=domain),
            ),
            y=alt.Y(
                "sum(n_diff)", title="Deceased", scale=alt.Scale(domain=[0, df.N.max()])
            ),
            order=alt.Order(
                # Sort the segments of the bars by this field
                "days_since_publication",
                sort="ascending",
            ),
            color=alt.Color(
                "lag:O",
                title="Lag in Days",
                sort=labels,
                scale=alt.Scale(scheme="category20c"),
            ),
        )
        .transform_filter(brush)
    )

    reported = (
        alt.Chart(df, height=100, width=800)
        .mark_bar()
        .encode(
            x=alt.X(
                "yearmonthdate(publication_date)",
                title="Publication Date",
                scale=alt.Scale(domain=domain),
            ),
            y=alt.Y("sum(n_diff)", title="Reported Deaths"),
            tooltip=[
                alt.Tooltip("sum(n_diff)", title="Reported Deaths"),
                "publication_date",
            ],
        )
        .add_selection(brush)
    )

    legend_vert = (
        alt.Chart(df, width=80, title="Lag in Days")
        .mark_bar()
        .encode(
            x=alt.X("sum(n_diff)", title="Reported Deaths"),
            y=alt.Y("lag", title="", sort=labels),
            color=alt.Color("lag:O", sort=labels, legend=None),
        )
        .transform_filter(brush)
    )

    text = (
        alt.Chart(df)
        .transform_filter(brush)
        .transform_aggregate(sum_deaths="sum(n_diff)")
        .transform_calculate(text="Total deaths: " + alt.datum.sum_deaths)
        .mark_text(align="right", x=792, y=19, fontSize=18)
        .encode(text="text:N")
    )

    prediction = (
        alt.Chart(df)
        .mark_bar(color="#E8E8E8")
        .encode(
            x="yearmonthdate(date)",
            y=alt.Y("prediction", aggregate={"argmax": "publication_date"}),
        )
        .transform_filter(brush)
    )

    chart = prediction + deceased + text & reported | legend_vert
    return chart


def daily_reported_deaths(df, labels):
    hist = (
        alt.Chart(df, height=100, width=100)
        .mark_bar()
        .encode(
            x=alt.X("lag:O", title="Reporting Lag", sort=labels),
            y=alt.Y("sum(n_diff):Q", title="Reported Deaths"),
            color=alt.Color(
                "day(publication_date):N", title="Publication Day", sort=["Mon"]
            ),
        )
    )

    text = (
        alt.Chart(df)
        .mark_text(align="right", x=95, y=28, fontSize=20)
        .encode(alt.Text("sum(n_diff)"),)
    )

    chart = (hist + text).facet(
        facet=alt.Facet("publication_date:T", title="Reported Deaths per Day"),
        columns=7,
    )

    return chart


def average_lag(df, start_date):
    df1 = pd.DataFrame(df.groupby("publication_date")["n_diff"].sum())
    df1["average_lag"] = (
        df.groupby("publication_date")["age"].sum()
        / df.groupby("publication_date")["n_diff"].sum()
    )
    df1 = df1.reset_index()
    df1 = df1[df1["publication_date"] >= start_date]

    lag_chart = (
        alt.Chart(df1, width=600, title="Average Reporting Lag")
        .mark_trail()
        .encode(
            x=alt.X("publication_date", title="Publication Date"),
            y=alt.Y("average_lag:Q", title="Daily Average Reporting Lag"),
            size=alt.Size("n_diff", title="Reported Deaths"),
        )
    )

    return lag_chart
