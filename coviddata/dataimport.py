import pandas as pd

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