import pandas as pd 

#set dytpes on load
mobility_cols = ["country_region_code", "sub_region_1", "date", "retail_and_recreation_percent_change_from_baseline", "grocery_and_pharmacy_percent_change_from_baseline", "parks_percent_change_from_baseline", "transit_stations_percent_change_from_baseline", "workplaces_percent_change_from_baseline", "residential_percent_change_from_baseline"]
mobility_dtypes = {"date": "str", "key": "str", "mobility_grocery_and_pharmacy": "float64", "mobility_parks": "float64", "mobility_transit_stations": "float64", "mobility_retail_and_recreation": "float64", "mobility_parks": "float64", "mobility_residential": "float64"}


#data
mobility = pd.read_csv("Global_Mobility_Report.csv", usecols = mobility_cols, dtype = mobility_dtypes)
codelookup = pd.read_csv("allcountrycodes.csv", usecols=["alpha-2", "alpha-3"])
eur = pd.read_csv("europeancodes.csv")

#fix date format
mobility['date'] = pd.to_datetime(mobility['date'], format='%Y-%m-%d')

#roll up  to national level only
mobility = mobility.loc[mobility['sub_region_1'].isnull()]

mobility["rolling_avg_parks"] = mobility.parks_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_retail_and_recreation"] = mobility.retail_and_recreation_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_grocery_and_pharmacy"] = mobility.grocery_and_pharmacy_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_workplaces"] = mobility.workplaces_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_transit_stations"] = mobility.transit_stations_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_residential"] = mobility.residential_percent_change_from_baseline.rolling(7).mean()

#rename country code columns for join
mobility = mobility.rename(columns={"country_region_code" : "alpha-2", "date" : "Date"})
codelookup = codelookup.rename(columns={"alpha-3" : "CountryCode"})


getcountrycode = pd.merge(mobility,
                        codelookup,
                        on = "alpha-2",
                        how = "left")


getcountrycode.to_csv("mobility_with_codes.csv")

#select europe

mobility_europe = pd.merge(eur,
                        getcountrycode,
                        on='CountryCode',
                        how = "left")

mobility_europe.drop(["Unnamed: 0", "alpha-2", 'sub_region_1'], axis = 1, inplace = True)

mobility_europe.to_csv("mobility_europe.csv")