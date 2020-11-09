import pandas as pd    

url = "https://raw.githubusercontent.com/ec-jrc/COVID-19/master/data-by-country/jrc-covid-19-all-days-by-country.csv"



eur = pd.read_csv("europeancodes.csv")
data = pd.read_csv(url)
data.rename(columns={'iso3':'CountryCode'}, inplace=True)


#add new cases and deaths daily
data["NewCases"] = data.groupby("CountryCode")["CumulativePositive"].diff()
data["NewDeaths"] = data.groupby("CountryCode")["CumulativeDeceased"].diff()
data["NewHospitalized"] = data.groupby("CountryCode")["Hospitalized"].diff()
data["NewICU"] = data.groupby("CountryCode")["IntensiveCare"].diff()

data["rolling_avg_new_cases"] = data.groupby("CountryCode")['NewCases'].rolling(7).mean().reset_index(0,drop=True)
data["rolling_avg_new_deaths"] = data.groupby("CountryCode")['NewDeaths'].rolling(7).mean().reset_index(0,drop=True)

data["new_cases_max"] = data.groupby("CountryCode")['NewCases'].transform(max)
data["new_cases_index"] = data["NewCases"]/data["new_cases_max"]

data["rolling_cases_max"] = data.groupby("CountryCode")['rolling_avg_new_cases'].transform(max)
data["rolling_cases_index"] = data["rolling_avg_new_cases"]/data["rolling_cases_max"]

print(data)

tester = data.loc[(data["CountryCode"] == "FRA")]
tester = tester[["Date", "NewCases", "new_cases_max", "new_cases_index", "rolling_cases_index"]]
tester.to_csv("testingnewcases.csv")

europedataonly = pd.merge(eur,
                        data,
                        on='CountryCode',
                        how = "left")

print(europedataonly)

newdf = europedataonly[["Date", "CountryCode", "NewCases", "NewDeaths", "NewHospitalized", "NewICU", "CumulativePositive", "CumulativeDeceased", "CurrentlyPositive", "IntensiveCare", "rolling_avg_new_cases", "rolling_avg_new_deaths", "new_cases_index", "rolling_cases_index"]].copy()




newdf.to_csv("europeancases.csv")