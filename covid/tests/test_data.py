from covid import dataimport
import pandas as pd


def test_fhm_data():
    fhm_data, labels = dataimport.get_fhm_data()
    assert all(
        fhm_data.columns
        == [
            "date",
            "N",
            "publication_date",
            "days_since_publication",
            "n_diff",
            "n_diff_pct",
            "delay",
            "lag",
            "age",
        ]
    )
    assert pd.api.types.is_datetime64_ns_dtype(fhm_data.date)
    assert pd.api.types.is_datetime64_ns_dtype(fhm_data.publication_date)
    assert labels[0] == "Same day"
