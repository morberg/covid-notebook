import pandas as pd
import locale


def get_lag_data():
    """
    Download data published by Folkhälsomyndigheten processed by @adamaltmejd

    Returns
    -------
    data : pandas.DataFrame
        Data containing Covid-19 related deaths in Sweden
    labels : array
        Labels for column 'lag' in data
    """

    bins = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 100]
    labels = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12+",
    ]

    date_cols = ["date", "publication_date"]
    df1 = pd.read_csv(
        "https://raw.githubusercontent.com/adamaltmejd/covid/master/data/covid_deaths_latest.csv",
        parse_dates=date_cols,
    ).set_index(["date", "publication_date"])

    df1["lag"] = pd.cut(df1["days_since_publication"], bins, labels=labels)
    df1["age"] = df1.days_since_publication * df1.n_diff

    date_cols = ["prediction_date", "date"]
    df2 = pd.read_csv(
        "https://raw.githubusercontent.com/adamaltmejd/covid/master/data/predictions.csv",
        parse_dates=date_cols,
    )

    df2 = df2.rename(
        columns={"prediction_date": "publication_date", "total.model": "prediction"}
    )
    df2 = df2.set_index(["date", "publication_date"])[["prediction"]]
    merged = pd.concat([df1, df2], axis=1, sort=False).reset_index()
    merged["publication_week"] = merged.publication_date.dt.week

    return merged, labels


def get_scb_county_data():
    """
    Download data published weekly by Statistiska Centralbyrån

    Returns
    -------
    data : pandas.DataFrame
        Data containing all deaths in Sweden 2018-2020 by county
    """

    # Needed to parse date strings from SCB
    locale.setlocale(locale.LC_ALL, "sv_SE")
    location = "https://scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/"

    rows_to_drop = [0, 1]
    data = pd.read_excel(
        location,
        sheet_name="Tabell 3",
        skiprows=5,
        header=1,
        usecols="A:W",
        na_values="..",
    )
    data["date"] = pd.to_datetime(
        data["Unnamed: 0"] + data["Year"].apply(str), format="%d %B%Y", errors="coerce"
    )
    data.drop(columns=["Unnamed: 0", "Year"], inplace=True)
    data.drop(rows_to_drop, inplace=True)
    data = data[:-3]  # The 3 last rows are a sum of all values

    rename_columns = {
        "Söderman-": "Södermanland",
        "Öster-": "Östergötland",
        "Västra": "Västra Götaland",
        "Västman-": "Västmanland",
        "Västernorr-": "Västernorrland",
        "Väster-": "Västerbotten",
        "Norr-": "Norrbotten",
    }
    data.rename(columns=rename_columns, inplace=True)

    data = data.melt("date", var_name="county", value_name="deaths")
    data.deaths = data.deaths.fillna(0).astype(int)

    return data


def merge_data(data_scb, data_fhm):
    """
    Merge data from SCB with data from FHM

    Returns
    -------
    data : pandas.DataFrame
        Data containing SCB and FHM statistics
    """
    scb = data_scb[data_scb.date.notna()].groupby("date").sum()
    fhm = data_fhm.set_index("date").max(level="date")[["N"]]

    data = pd.concat([scb, fhm], axis=1, sort=False)
    data = data[data.index.notna()]
    data.columns = [
        "non-covid",
        "covid",
    ]
    # 'non-covid' currently contains total number of deaths
    data["non-covid"] = data["non-covid"].fillna(0) - data["covid"].fillna(0)
    data = data.reset_index()
    data = data.melt("date", var_name="death_cause", value_name="deaths")
    data = data.fillna(0)

    # FHM data is newer than SCB which will result in "negative" deaths in the tail
    return data.loc[data.deaths >= 0]
