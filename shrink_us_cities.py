import pandas as pd
import pdb
import pickle
import app

# chunk in the csv 
chunk = pd.read_csv('uscities.csv', chunksize=1000)
df = pd.concat(chunk)
df = df.reset_index()  # make sure indexes pair with number of rows
all_cities = {}
# get us city state and set entry in dict
for index, row in df.iterrows():
    city	=  row["city"].lower()
    state 	= row["state_id"].lower()
    city_state = city + state
    lat 	= row["lat"]
    lng 	= row["lng"]
    lat_lng = str(lat) + "," + str(lng)
    all_cities[city_state] = lat_lng

# write hash table to file
w_file = open('uscities', 'wb')
pickle.dump(all_cities, w_file)





