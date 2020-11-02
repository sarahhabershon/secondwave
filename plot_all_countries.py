import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_csv("eurosample.csv")

data.drop_duplicates()

data.groupby("CountryName").plot


def makeCharts(x):
    plt.clf()
    # country = data.loc[data['CountryName'] == x, data['RegionCode'].isnull()]
    country = data.loc[((data['CountryName'] == x) & (data['RegionCode'].isnull()))]
    print(country)
    name = country["CountryName"]
    country['stringency_index'] = country['StringencyIndexForDisplay']/100

    plt.plot("Date", "openness_risk", data=country, marker='', linewidth=2)
    plt.plot("Date", "stringency_index", data=country, marker='', linewidth=2)
    plt.title(str(x))
    plt.legend()
    plt.savefig("chart " + str(x) + ".png")

    

toplot = data['CountryName'].drop_duplicates()


toplot.apply(makeCharts)