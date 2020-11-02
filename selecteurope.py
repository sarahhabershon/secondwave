import pandas as pd 

eur = pd.read_csv("europeancodes.csv")

mydata = pd.read_csv('joined.csv')

europedataonly = pd.merge(eur,
                        mydata,
                        on='CountryCode',
                        how = "left")

europedataonly.drop(["name", "Unnamed: 0_x", "Unnamed: 0_y"], axis = 1, inplace = True)

print(europedataonly)

europedataonly.to_csv("eurosample.csv")