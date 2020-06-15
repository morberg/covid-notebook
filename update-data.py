from covid import dataimport

fhm_file = "data/fhm.json"
scb_file = "data/scb.json"
combined_file = "data/combined.json"

fhm_data, _ = dataimport.get_lag_data()
fhm_data.to_json(fhm_file, orient="records")

scb_data = dataimport.get_scb_county_data()
weekly = scb_data.groupby("county").resample("W", on="date").sum().reset_index()

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

data_combined = dataimport.merge_data(scb_data, fhm_data)
data_combined = (
    data_combined.groupby("death_cause").resample("W", on="date").sum().reset_index()
)
data_combined.to_json(combined_file, orient="records")
