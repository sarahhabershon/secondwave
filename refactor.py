import pandas as pd 
import io


#colunns and dtypes
#risk and stringency data
riskcols = ['Date', 'CountryCode', 'CountryName', 'openness_risk']
stringencycols = ['Date', 'CountryCode', 'RegionCode', 'StringencyIndex', 'StringencyIndexForDisplay']
risk_dtypes = {"CountryCode": "str", "CountryName": "str", "openness_risk": "float64"}
stringency_dtypes = {"CountryCode": "str", "RegionCode" : "str", "StringencyIndex": "float64", "StringencyIndexForDisplay": "float64"}
# mobility data
mobility_cols = ["country_region_code", "sub_region_1", "date", "retail_and_recreation_percent_change_from_baseline", "grocery_and_pharmacy_percent_change_from_baseline", "parks_percent_change_from_baseline", "transit_stations_percent_change_from_baseline", "workplaces_percent_change_from_baseline", "residential_percent_change_from_baseline"]
mobility_dtypes = {"date": "str", "key": "str", "mobility_grocery_and_pharmacy": "float64", "mobility_parks": "float64", "mobility_transit_stations": "float64", "mobility_retail_and_recreation": "float64", "mobility_parks": "float64", "mobility_residential": "float64"}


#sources risk and stringency
risk_url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-scratchpad/master/risk_of_openness_index/data/riskindex_timeseries_latest.csv"
stringency_url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"

#source_cases
ecjrc_url = "https://raw.githubusercontent.com/ec-jrc/COVID-19/master/data-by-country/jrc-covid-19-all-days-by-country.csv"

#source mobility
mobility = pd.read_csv("Global_Mobility_Report.csv", usecols = mobility_cols, dtype = mobility_dtypes, parse_dates = ["date"])

#source geo
eur = pd.read_csv("europeancodes.csv")
codelookup = pd.read_csv("allcountrycodes.csv", usecols=["alpha-2", "alpha-3"])

#load risk and stringency and parse dates
risk_data = pd.read_csv(risk_url, usecols = riskcols, parse_dates=["Date"],  dtype = risk_dtypes)
stringency_data = pd.read_csv(stringency_url, usecols = stringencycols, parse_dates=["Date"], dtype = stringency_dtypes)

#add daily new cases/deaths and add rolling averages
case_data = pd.read_csv(ecjrc_url, parse_dates=["Date"])
case_data.rename(columns={'iso3':'CountryCode'}, inplace=True)
case_data["NewCases"] = case_data.groupby("CountryCode")["CumulativePositive"].diff()
case_data["NewDeaths"] = case_data.groupby("CountryCode")["CumulativeDeceased"].diff()
case_data["NewHospitalized"] = case_data.groupby("CountryCode")["Hospitalized"].diff()
case_data["NewICU"] = case_data.groupby("CountryCode")["IntensiveCare"].diff()

case_data["rolling_avg_new_cases"] = case_data.groupby("CountryCode")['NewCases'].rolling(7).mean().reset_index(0,drop=True)
case_data["rolling_avg_new_deaths"] = case_data.groupby("CountryCode")['NewDeaths'].rolling(7).mean().reset_index(0,drop=True)

case_data["new_cases_max"] = case_data.groupby("CountryCode")['NewCases'].transform(max)
case_data["new_cases_index"] = case_data["NewCases"]/case_data["new_cases_max"]

case_data["rolling_cases_max"] = case_data.groupby("CountryCode")['rolling_avg_new_cases'].transform(max)
case_data["rolling_cases_index"] = case_data["rolling_avg_new_cases"]/case_data["rolling_cases_max"]


#rename cols for join
mobility = mobility.rename(columns={"country_region_code" : "alpha-2", "date" : "Date"})
codelookup = codelookup.rename(columns={"alpha-3" : "CountryCode"})

#roll mobility to national level and add rolling averages
mobility = mobility.loc[mobility['sub_region_1'].isnull()]

mobility["rolling_avg_parks"] = mobility.parks_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_retail_and_recreation"] = mobility.retail_and_recreation_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_grocery_and_pharmacy"] = mobility.grocery_and_pharmacy_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_workplaces"] = mobility.workplaces_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_transit_stations"] = mobility.transit_stations_percent_change_from_baseline.rolling(7).mean()
mobility["rolling_avg_residential"] = mobility.residential_percent_change_from_baseline.rolling(7).mean()

# add country codes and select europe
getcountrycode = pd.merge(mobility,
                        codelookup,
                        on = "alpha-2",
                        how = "left")

mobility_europe = pd.merge(eur,
                        getcountrycode,
                        on='CountryCode',
                        how = "left")

mobility_europe.drop(["Unnamed: 0", "alpha-2", 'sub_region_1'], axis = 1, inplace = True)


#join risk and stringency
join_stringency_risk = pd.merge(stringency_data,
						risk_data,
						on=["Date", "CountryCode"],
						how = "inner")
# print(join_stringency_risk.dtypes)

#create a subset for Europe
europe_risk_stringency = pd.merge(eur,
                        join_stringency_risk,
                        on='CountryCode',
                        how = "left")

europe_risk_stringency.drop(["name", "Unnamed: 0"], axis = 1, inplace = True)

# print(europe_risk_stringency.dtypes)
#join risk and stringency to cases

print(case_data.dtypes)
# print(europe_risk_stringency.dtypes)

europe_risk_stringency_cases = pd.merge(case_data,
                    europe_risk_stringency,
                    on=["Date", "CountryCode"],
                    how = "left")

total_join = pd.merge(europe_risk_stringency_cases,
                    mobility_europe,
                    on=["Date", "CountryCode"],
                    how = "left")

total_join.to_csv("refactored_output.csv")