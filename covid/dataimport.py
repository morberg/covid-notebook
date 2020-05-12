import pandas as pd
import locale

def get_fhm_data():
    """
    Download data published by Folkhälsomyndigheten processed by @adamaltmejd

    Returns
    -------
    data : pandas.DataFrame
        Data containing Covid-19 related deaths in Sweden
    labels : array
        Labels for column 'lag' in data
    """

    bins = [-1,0,1,2,3,4,5,6,7,8,9,10,11,100]
    labels = ['Same day','1','2','3','4','5','6','7','8','9','10','11','12+']

    date_cols = ['date', 'publication_date']
    data = pd.read_csv('https://raw.githubusercontent.com/adamaltmejd/covid/master/data/covid_deaths_latest.csv', parse_dates=date_cols)

    data['lag'] = pd.cut(data['days_since_publication'], bins, labels=labels)
    data['age'] = data.days_since_publication * data.n_diff
    return data, labels

def get_scb_county_data():
    """
    Download data published weekly by Statistiska Centralbyrån

    Returns
    -------
    data : pandas.DataFrame
        Data containing all deaths in Sweden 2018-2020 by county
    """

    # Needed to parse date strings from SCB
    locale.setlocale(locale.LC_ALL, 'sv_SE'
    ) 
    location="https://scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/"

    rows_to_drop = [0, 1]
    data = pd.read_excel(location, sheet_name="Tabell 3", skiprows=5, header=1, usecols='A:W', na_values="..")
    data['date'] = pd.to_datetime(data['Unnamed: 0'] + data['Year'].apply(str), format='%d %B%Y', errors='coerce')
    data.drop(columns=['Unnamed: 0', 'Year'], inplace=True)
    data.drop(rows_to_drop, inplace=True)
    data = data[:-3] # The 3 last rows are a sum of all values

    rename_columns = {'Söderman-':'Södermanland', 'Öster-': 'Östergötland', 'Västra': 'Västra Götaland', 'Västman-': 'Västmanland', 'Västernorr-': 'Västernorrland', 'Väster-': 'Västerbotten', 'Norr-': 'Norrbotten'}
    data.rename(columns=rename_columns, inplace=True)

    data = data.melt('date', var_name='county', value_name='deaths')
    data.deaths = data.deaths.fillna(0).astype(int)

    return data
