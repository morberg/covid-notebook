from covid import dataimport
import pandas as pd


def test_lag_data():
    lag_data, labels = dataimport.get_lag_data()
    assert all(
        lag_data.columns
        == [
            "date",
            "publication_date",
            "N",
            "days_since_publication",
            "n_diff",
            "n_diff_pct",
            "delay",
            "lag",
            "age",
            "prediction",
            "publication_week",
        ]
    )
    assert pd.api.types.is_datetime64_ns_dtype(lag_data.date)
    assert pd.api.types.is_datetime64_ns_dtype(lag_data.publication_date)
    assert labels[0] == "0-1"
