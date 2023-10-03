
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import fetching
import trips
import runner

#global variables
release=2023
firsturl=f"https://www.imdb.com/search/title/?title_type=feature,tv_series&year=2023-01-01,2023-12-31&explore=countries&countries=IN"
recordsinimdb=2200


def main():

    start_time = time.time()
    #csv name
    runner.fetch('z1',firsturl,recordsinimdb,release)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)


if __name__ == "__main__":
    main()