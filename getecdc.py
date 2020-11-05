import pandas as pd    

url = "https://raw.githubusercontent.com/ec-jrc/COVID-19/master/data-by-country/jrc-covid-19-all-days-by-country.csv"

eur = pd.read_csv("europeancodes.csv")

# data = pd.read_csv("ecdcdailyasat10October.csv")

# data.to_csv("ecdcdailyasat10October.csv")

data = pd.read_csv(url)
data.rename(columns={'iso3':'CountryCode'}, inplace=True)

print(data)


europedataonly = pd.merge(eur,
                        data,
                        on='CountryCode',
                        how = "left")

print(europedataonly)

newdf = europedataonly[["Date", "CountryCode", "CumulativePositive", "CumulativeDeceased", "CurrentlyPositive", "IntensiveCare"]].copy()

newdf.to_csv("europeancases.csv")