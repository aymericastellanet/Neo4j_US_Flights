import pandas as pd

#by Aymeric Castellanet

## Import the two dataframes and merge them
df_left = pd.read_csv("International_Report_Passengers.csv")
df_right = pd.read_csv("major_airlines_codes.csv")

df = df_left.merge(df_right, how="left", left_on="carrier", right_on="carrier_2_letters")


## Select only the columns we want to keep, rename columns, and order the DataFrame
df = df[["data_dte", "Year", "Month", "usg_apt", "fg_apt", "carrier", "airline", "country", "Scheduled", "Charter", "Total"]]

df = df.rename(columns={"data_dte": "Date", "usg_apt": "US_Airport", "fg_apt": "Foreign_Airport",
	"carrier": "Airline_Code", "airline": "Airline_Name", "country": "Airline_Country", 
	"Scheduled": "Nb_Passengers_Scheduled", "Charter": "Nb_Passengers_Charter", "Total": "Nb_Passengers_Total"})

df = df.sort_values(by=["Year", "Month", "Nb_Passengers_Total"], ascending=True)


## Print the resulting DataFrame ##
print("Shape of the table:", df.shape)
print(df.head(25))
print(df.tail(25))


## Export the resulting DataFrame to a csv file ##
df.to_csv("US_international_flights_1990_2020.csv", index=False)

print("Export completed!")