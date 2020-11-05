import pandas as pd 

eur_risk_strin = pd.read_csv("europe_joined.csv")
goog_mob = pd.read_csv("mobility_europe.csv")

#dates to datetime
goog_mob['Date'] = pd.to_datetime(goog_mob['Date'], format='%Y-%m-%d')
eur_risk_strin['Date'] = pd.to_datetime(eur_risk_strin['Date'], format='%Y-%m-%d')




test = pd.merge(eur_risk_strin,
                goog_mob,
                on=["Date", "CountryCode"],
                how = "inner")



print(test.head)

test.to_csv("zzdiditwork.csv")