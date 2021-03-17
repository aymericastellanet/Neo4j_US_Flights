from neo4j import GraphDatabase
from time import time

#by Aymeric Castellanet

"""
First you need to launch the docker container: 
docker run -p 7474:7474 -p 7687:7687 --name my_neo4j aymericastellanet/neo4j

Then open a web browser and enter the following adress:
http://localhost:7474/ to access the Neo4j Browser
and if needed, log in with the username and password: 'neo4j'

Finally you can run this file to fill the Neo4j database 
with the US Flights data from 1990 to 2020: 
python3 load_US_flights_db_neo4j.py

Then you can try some queries like:
MATCH (a1:Airport) WHERE a1.Country = "France"
MATCH (a2:Airport) WHERE a2.Location CONTAINS "New York"
MATCH (a1)-[r:FLIGHTS]-(a2)
RETURN a1, a2;
"""

driver = GraphDatabase.driver("bolt://0.0.0.0:7687",
                              auth=("neo4j", "neo4j"))

t0 = time()

# Deleting previous data
print("Deleting previous data...")

query = """
MATCH (n) 
DETACH DELETE n
"""

with driver.session() as session:
    print(query)
    session.run(query)

t1 = time()

print("...done in {} seconds!".format(round(t1-t0, 2))) #less than 10 seconds


# Inserting data
print("Inserting airports...")

query = """
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/aymericastellanet/Neo4j_US_Flights/master/iata_code_airports.csv' AS row
CREATE (:Airport {Name: row.Name, IATA_code: row.IATA, ICAO_code: row.ICAO,
  Location: row.City, Country: row.Country
  });
  """

with driver.session() as session:
    print(query)
    session.run(query)

t2 = time()

print("...done in {} seconds!".format(round(t2-t1, 2))) #less than 5 seconds


# Inserting flights relationships between a pair of airports
print("Inserting flights...")

query = """
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/aymericastellanet/Neo4j_US_Flights/master/US_international_flights_1990_2020.csv' AS row
MATCH (a_us:Airport) WHERE a_us.IATA_code = row.US_Airport
MATCH (a_fg:Airport) WHERE a_fg.IATA_code = row.Foreign_Airport
CREATE (a_us)-[:FLIGHT {
  Date: toString(row.Date), Year: toInteger(row.Year), Month: toInteger(row.Month), Airline_Code: row.Airline_Code,
  Airline_Name: row.Airline_Name, Airline_Country: row.Airline_Country, Nb_Passengers_Scheduled: toInteger(row.Nb_Passengers_Scheduled),
  Nb_Passengers_Charter: toInteger(row.Nb_Passengers_Charter), Nb_Passengers_Total: toInteger(row.Nb_Passengers_Total)
  }]->(a_fg);
  """

with driver.session() as session:
    print(query)
    session.run(query)

t3 = time()

print("...done in {} seconds!".format(round(t3-t2, 2))) #can take more than 1 hour (~ 3700 seconds)