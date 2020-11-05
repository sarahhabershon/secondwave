import pandas as pd 
import matplotlib.pyplot as plt


data = pd.read_csv("mobility_stringency_match.csv", parse_dates =["Date"])

data.groupby("name").plot

def makeCharts(x):
    plt.clf()
    country = data.loc[data['name'] == str(x)]
    name = country["name"]
    country = data.loc[((data['name'] == x) & (data['RegionCode'].isnull()))]
    country['openness_risk'] = country['openness_risk']*100
    plt.plot("Date", "openness_risk", data=country, marker='', linewidth=2)
    plt.plot("Date", "StringencyIndex", data=country, marker='', linewidth=2)
    # plt.plot("Date", "retail_and_recreation_percent_change_from_baseline", data=country, marker='', linewidth=2)
    plt.plot("Date", "rolling_avg_retail_and_recreation", data=country, marker='', linewidth=2)
    # # # plt.plot("Date", "workplaces_percent_change_from_baseline", data=country, marker='', linewidth=2)
    plt.plot("Date", "rolling_avg_workplaces", data=country, marker='', linewidth=2)
    # # # plt.plot("Date", "grocery_and_pharmacy_percent_change_from_baseline", data=country, marker='', linewidth=2)
    plt.plot("Date", "rolling_avg_grocery_and_pharmacy", data=country, marker='', linewidth=2)
    # # # plt.plot("Date", "parks_percent_change_from_baseline", data=country, marker='', linewidth=2)
    plt.plot("Date", "rolling_avg_parks", data=country, marker='', linewidth=2)
    # # # plt.plot("Date", "transit_stations_percent_change_from_baseline", data=country, marker='', linewidth=2)
    plt.plot("Date", "rolling_avg_transit_stations", data=country, marker='', linewidth=2)
    # # # plt.plot("Date", "residential_percent_change_from_baseline", data=country, marker='', linewidth=2)
    plt.plot("Date", "rolling_avg_residential", data=country, marker='', linewidth=2)
    plt.title(str(x))
    plt.legend()
    plt.show()
    # plt.savefig("mobility " + str(x) + ".png")



    

toplot = data["name"].drop_duplicates()

toplot.apply(makeCharts)
