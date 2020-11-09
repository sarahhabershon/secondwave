import pandas as pd 

eur_risk_strin = pd.read_csv("europe_joined.csv", parse_dates =["Date"])
goog_mob = pd.read_csv("mobility_europe.csv", parse_dates =["Date"])
cases = pd.read_csv("europeancases.csv", parse_dates =["Date"])

#dates to datetime
goog_mob['Date'] = pd.to_datetime(goog_mob['Date'], format='%Y-%m-%d')
eur_risk_strin['Date'] = pd.to_datetime(eur_risk_strin['Date'], format='%Y-%m-%d')
cases['Date'] = pd.to_datetime(cases['Date'], format='%Y-%m-%d')

join_one = pd.merge(cases,
                    eur_risk_strin,
                    on=["Date", "CountryCode"],
                    how = "left")

join_two = pd.merge(join_one,
                    goog_mob,
                    on=["Date", "CountryCode"],
                    how = "left")

# join_one = pd.merge(eur_risk_strin,
#                 goog_mob,
#                 on=["Date", "CountryCode"],
#                 how = "inner")


# join_one.to_csv("mobility_stringency_match.csv")

# join_two = pd.merge(join_one,
#             cases,
#             on = ["Date", "CountryCode"],
#             how = "inner")



join_two.to_csv("total_merge_version_two.csv")