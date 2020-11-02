import pandas as pd 

url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"

countrycodes = pd.read_csv(url)


countrycodes.to_csv("allcountrycodes.csv")

europe = countrycodes.loc[countrycodes['region'] == 'Europe']
europefile = europe.filter(['alpha-3', 'name'], axis = 1)

europefile.to_csv('europeancodes.csv')