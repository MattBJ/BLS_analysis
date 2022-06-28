import numpy as np
import pandas as pd
# import requests

import requests
import json
import prettytable

# https://www.bd-econ.com/blsapi.html

# base url for BLS API v2
url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

import secrets

key = '?registrationkey={}'.format(secrets.api_key)

# series stored as a dictionary
series_dict = {
	'LNS14000003': 'White',
	'LNS14000006': 'Black',
	'LNS14000009': 'Hispanic'
}

# Start year and end year
dates = ('2008', '2017')

headers = {'Content-type':'application/json'}

data = json.dumps(
	{
		"seriesid": list(series_dict.keys()),
		"startyear":dates[0],
		"endyear":dates[1]
	}
)

response = requests.post(
		'{}{}'.format(url,key),
		headers=headers,
		data=data
	)
p = response.json()['Results']['series']

# Date index from first series
date_list = [f"{i['year']}-{i['period'][1:]}-01" for i in p[0]['data']]

# Empty dataframe to fill with values
df = pd.DataFrame()

# Build a pandas series from the API results, p
for s in p:
	df[series_dict[s['seriesID']]] = pd.Series(
			index = pd.to_datetime(date_list),
			data = [i['value'] for i in s['data']]
		).astype(float).iloc[::-1]

# Show last 5 results
df.tail()