import pandas as pd 

eur = pd.read_csv("europeancodes.csv")

risk_and_stringency = pd.read_csv('joined.csv')
risk_stringency_mobility = pd.read_csv("joined_with_mobility.csv")

# europedataonly = pd.merge(eur,
#                         risk_and_stringency,
#                         on='CountryCode',
#                         how = "left")

# europedataonly.drop(["name", "Unnamed: 0_x", "Unnamed: 0_y"], axis = 1, inplace = True)

# print(europedataonly)

# europedataonly.to_csv("eurosample.csv")


europe_with_mobility = pd.merge(eur,
                        risk_stringency_mobility,
                        on='CountryCode',
                        how = "left")

europe_with_mobility.drop(["name", "Unnamed: 0_x", "Unnamed: 0_y"], axis = 1, inplace = True)

# europedataonly.drop(["name", "Unnamed: 0_x", "Unnamed: 0_y"], axis = 1, inplace = True)

europe_with_mobility.to_csv("europe_mobility.csv")