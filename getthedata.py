import pandas as pd 
import io
import requests


risk_url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-scratchpad/master/risk_of_openness_index/data/riskindex_timeseries_latest.csv"
stringency_url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
eur = pd.read_csv("europeancodes.csv")

#set dytpes on load
risk_dtypes = {"CountryCode": "str", "CountryName": "str", "openness_risk": "float64"}
stringency_dtypes = {"CountryCode": "str", "RegionCode" : "str", "StringencyIndex": "float64", "StringencyIndexForDisplay": "float64"}


risk_data = pd.read_csv(risk_url).astype(risk_dtypes)
stringency_data = pd.read_csv(stringency_url).astype(stringency_dtypes)

# risk_data.to_csv("completerawrisk.csv")
# stringency_data.to_csv("completerawstringency.csv")

#unify date format
risk_data['Date'] = pd.to_datetime(risk_data['Date'], format='%Y-%m-%d')
stringency_data['Date'] = pd.to_datetime(stringency_data['Date'], format='%Y%m%d')

#reduce number of columns
stringency_short = stringency_data[['Date', 'CountryCode', 'RegionCode', 'StringencyIndex', 'StringencyIndexForDisplay']].copy()
risk_short = risk_data[['Date', 'CountryCode', 'CountryName', 'openness_risk']].copy()


print(risk_short.dtypes)
print(stringency_short.dtypes)

risk_short.to_csv('rawriskindexdata.csv')
stringency_short.to_csv('rawstringency.csv')


jointables = pd.merge(stringency_short,
						risk_short,
						on=["Date", "CountryCode"],
						how = "inner")


jointables.to_csv("joined.csv")


#create a subset for Europe
europedataonly = pd.merge(eur,
                        jointables,
                        on='CountryCode',
                        how = "left")

europedataonly.drop(["name", "Unnamed: 0"], axis = 1, inplace = True)

europedataonly.to_csv("europe_joined.csv")
