import trips
import pandas as pd

def fetch(csv,firsturl,recordsinimdb,release):
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