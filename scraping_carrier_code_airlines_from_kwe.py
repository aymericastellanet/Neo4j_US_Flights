from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

#by Aymeric Castellanet

kwe_page = urlopen("https://www.kwe.co.jp/en/useful-contents/code1")

soup = BeautifulSoup(kwe_page, 'html.parser')

## Scrap Airlines names ##
airline_kwe = soup.select("tr+ tr td:nth-child(2)")

airline = []
for element in airline_kwe:
	#Capitalize every word in the airline name
	airl = element.text
	airl_capitalize = ""
	for string in airl.split(" "):
		string = string.capitalize()
		airl_capitalize +=  string + " "
	airl_capitalize = airl_capitalize.strip()
	airline.append(airl_capitalize)


## Scrap Airlines country ##
country_kwe = soup.select("tr+ tr td:nth-child(3)")

country = []
for element in country_kwe:
	cntry = element.text
	#Capitalize every word in the country
	if "." not in cntry:
		cntry_capitalize = ""
		for string in cntry.split(" "):
			string = string.capitalize()
			cntry_capitalize += string + " "
		cntry_capitalize = cntry_capitalize.strip()
	else: #if country = 'U.K.', 'U.S.A.' or 'U.A.E.'
		cntry_capitalize = cntry
	country.append(cntry_capitalize)


## Scrap Carrier codes with 2 letters ##
carrier2_kwe = soup.select("tr+ tr td:nth-child(4)")

carrier2 = []
for element in carrier2_kwe:
	carrier2.append(element.text.upper())


## Scrap Carrier codes with 3 letters ##
carrier3_kwe = soup.select("tr+ tr td:nth-child(5)")

carrier3 = []
for element in carrier3_kwe:
	carrier3.append(element.text.upper())


## Save scraped data into a DataFrame ## 
df = pd.DataFrame({
	"airline": airline, 
	"country": country, 
	"carrier_2_letters": carrier2, 
	"carrier_3_letters": carrier3
	})


## Print the resulting DataFrame ##
print("Shape of the table:", df.shape)
print(df.head(10))
print(df.tail(10))


## Export the resulting DataFrame to a csv file ##
df.to_csv("major_airlines_codes.csv", index=False)

print("Export completed!") 