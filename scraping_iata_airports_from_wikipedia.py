from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

#by Aymeric Castellanet

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

url = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"

list_df = [] #data for each page will be save into a DataFrame

for letter in alphabet: #loop on the 26 wikipedia pages
	wiki_page = urlopen(url+letter)

	soup = BeautifulSoup(wiki_page, 'html.parser')

	## Scrap IATA codes ##
	iata_wiki = soup.select("td:nth-child(1)")

	iata = []
	for element in iata_wiki:
		string = element.text
		if len(string) != 0 and len(string) > 3:
			string = string[:3] #to remove the references numbers: 'BAK[1]' -> 'BAK'
		iata.append(string)


	## Scrap ICAO codes ##
	icao_wiki = soup.select("td:nth-child(2)")

	icao = []
	for element in icao_wiki:
		string = element.text
		if len(string) != 0 and len(string) > 4:
			string = string[:4] #to remove the references numbers: 'SWTU[4]' -> 'SWTU'
		icao.append(string)

	#We remove the last elements which are not in the main table but in the table 'List of airports' in the 'References' paragraph
	icao = icao[:len(iata)]


	## Scrap Airports names ##
	airport_wiki = soup.select("td:nth-child(3)")

	airport = []
	for element in airport_wiki:
		string = element.text
		#if there is a reference number at the end '[1]', we remove it:
		if '[' in string:
			string = string[:string.find('[')]
		#if there is a FAA code at the end '(FAA: JZZ)', we remove it:
		if '(FAA' in string:
			string = string[:string.find('(FAA')]
		#if there is a TC code at the end '(TC: CFC4)', we remove it:
		if '(TC' in string:
			string = string[:string.find('(TC')]
		airport.append(string)


	## Scrap Locations of the airports ##
	location_wiki = soup.select("td:nth-child(4)")

	location = []
	for element in location_wiki:
		string = element.text
		string = string.strip()
		location.append(string)


	## Save scraped data into a DataFrame ## 
	df = pd.DataFrame({
		"IATA": iata, "ICAO": icao, 
		"Name": airport, "Location": location
		})

	list_df.append(df)


## Create the DataFrame with all the rows from the 26 scraped pages ##
df_final = pd.DataFrame(columns=["IATA", "ICAO", "Name", "Location"])

for df in list_df:
	df_final = df_final.append(df, ignore_index=True)


## Create the 'country' and 'city' columns from 'location'
list_country = []
list_city = []

for location in list(df_final["Location"].values):
	#Retrieve the country at the end of 'location'
	country = location.split(',')[-1]
	country = country.strip()
	list_country.append(country)

	#Retrieve the city (with eventually the state) written before the country
	city = ""
	for string in location.split(',')[:-1]:
		city += string + ','
	city = city[:-1] #remove the last character which is a comma
	list_city.append(city)


# Add 'country' and 'city' columns to the final DataFrame
df_final["Country"] = list_country
df_final["City"] = list_city

# Remove the 'location' column
df_final = df_final.drop("Location", axis=1)


## Print the resulting DataFrame ##
print("Shape of the table:", df_final.shape)
print(df_final.head(25))
print(df_final.tail(25))


## Export the resulting DataFrame to a csv file ##
df_final.to_csv("iata_code_airports.csv", index=False)

print("Export completed!") 