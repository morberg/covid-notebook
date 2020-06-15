from covid import dataimport

scb_file = "data/scb.json"
combined_file = "data/combined.json"

data_scb = dataimport.get_scb_county_data()
weekly = data_scb.groupby("county").resample("W", on="date").sum().reset_index()

# Calculate cumulative deaths per county, reset each year
weekly = weekly.dropna().sort_values(by=["county", "date"]).set_index("date")
cum_deaths = (
    weekly.groupby(["county", "date"])
    .sum()
    .groupby(by=[weekly.index.year, "county"])
    .cumsum()
)
weekly = weekly.reset_index()
weekly["cumulative_deaths"] = cum_deaths.reset_index()["deaths"]
weekly.to_json(scb_file, orient="records")

data_fhm, _ = dataimport.get_lag_data()
data_combined = dataimport.merge_data(data_scb, data_fhm)
data_combined.to_json(combined_file, orient="records")
