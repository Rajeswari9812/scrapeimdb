
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import fetching
import trips

#global variables
release=2023
firsturl=f"https://www.imdb.com/search/title/?title_type=feature,tv_series&year=2023-01-01,2023-12-31&explore=countries&countries=IN"
recordsinimdb=2200


def fetch(csv):
# First, call trip1 to create the initial CSV
    trips.tripone(f'{csv}',firsturl,release)
    # Then, call resttrips to append data to the CSV
    trips.resttrips(f'{csv}', totalentries=recordsinimdb)
    #add index
    df = pd.read_csv(f'{csv}.csv')
    # Add an index column to the DataFrame
    df.insert(0, 'Index', range(1, len(df) + 1))
    # Save the DataFrame with the added index back to a CSV file
    df.to_csv(f'{csv}.csv', index=False)

def main():

    start_time = time.time()
    #csv name
    fetch('z1')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)


if __name__ == "__main__":
    main()