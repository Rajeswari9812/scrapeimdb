
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame


#global variables
release=2023
firsturl=f"https://www.imdb.com/search/title/?title_type=feature,tv_series&year=2023-01-01,2023-12-31&explore=countries&countries=IN"
recordsinimdb=2200


# Send an HTTP GET request to the URL
def gettingdata(release,uri):

    response = requests.get(uri)
    finallist=[]
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the movie items on the page
        movie_items = soup.find_all('div', class_='lister-item-content')

        for movienumber, movie_item in enumerate(movie_items, start=1):
            movie_dets = []

            # Extract movie name and ttn
            try:
                name_ttn = movie_item.find('h3', class_='lister-item-header').find('a')
                ttn=name_ttn.get('href').split(sep='/')[2]
                movie_dets.append(ttn)

                names = name_ttn.text if name_ttn else 'Null'
                movie_dets.append(names)
            except:
                movie_dets.append('null')

            # Extract duration
            try:
                duration = movie_item.find('span', class_='runtime')
                durations = duration.text if duration else 'Null'
                movie_dets.append(durations)
            except:
                movie_dets.append(ratings)


            # Extract description
            try:
                # Find the desired element using CSS selector
                desc = soup.select_one(
                    f'#main > div > div.lister.list.detail.sub-list > div > div:nth-child({movienumber}) > div.lister-item-content > p:nth-child(4)')

                if desc and desc!='Add a Plot':
                    descs = desc.get_text(strip=True)
                    movie_dets.append(descs)
                else:
                    movie_dets.append('Null')
            except:
                movie_dets.append('Null')

            reldate = release
            movie_dets.append(reldate)

            # Extract genre
            try:
                genre = movie_item.find('span', class_='genre')
                genres = genre.text.strip().split(', ') if genre else 'Null'
                movie_dets.append(genres)
            except:
                movie_dets.append(ratings)

            # Extract director and actors
            try:
                team = soup.select_one(
                    f'#main > div > div.lister.list.detail.sub-list > div > div:nth-child({movienumber}) > div.lister-item-content > p:nth-child(5)').get_text()
                if team.find('Director'):
                    team = team.replace('\n', '')
                    spl1 = team.split(sep='|')
                    director = spl1[0].split('Director:')[1]
                    if director != '':
                        movie_dets.append(director)
                    else:
                        movie_dets.append('Null')
                    director=''


            except:
                movie_dets.append('Null')

            try:
                if team.find("Stars"):
                    castlist = spl1[1].split('Stars:')[1].split(sep=',')
                    movie_dets.append(castlist)
                    castlist=[]
            except:
                movie_dets.append('Null')

            try:
                vote = soup.select_one(
                    f'#main > div > div.lister.list.detail.sub-list > div > div:nth-child({movienumber}) > div.lister-item-content > p.sort-num_votes-visible > span:nth-child(2)').get_text()
                movie_dets.append(vote)
            except:
                movie_dets.append('Null')

            # Extract rating
            try:
                rating = movie_item.find('strong')
                ratings = rating.text if rating else 'Null'
                movie_dets.append(ratings)
            except:
                movie_dets.append(ratings)



            finallist.append(movie_dets)



        # Create a DataFrame and save to CSV

        return finallist


# df = pd.DataFrame(finallist, columns=["Name", "Duration", "Description", "year", "Genre", "director", "actors", "votes", "rating"])
# df.to_csv("nested_data6.csv", index=True)


def trip1(csvname):
    url = "https://www.imdb.com/search/title/?title_type=feature,tv_series&year=2023-01-01,2023-12-31&explore=countries&countries=IN"
    finalist = gettingdata(2023, url)
    df = pd.DataFrame(finalist,
                      columns=["Name", "Duration", "Description", "year", "Genre", "director", "actors", "votes",
                               "rating"])
    df.to_csv(f"{csvname}.csv", index=False)



import pandas as pd

def trip1(csvname,firsturl):
    url = firsturl
    finalist = gettingdata(release, url)
    df = pd.DataFrame(finalist,
                      columns=["TTN","Name", "Duration", "Description", "year", "Genre", "director", "actors", "votes", "rating"])
    df.to_csv(f"{csvname}.csv", index=False)

def resttrips(csvname, totalentries):
    for i in range(51, totalentries, 50):
        try:
            # Read the existing CSV file
            existing_df = pd.read_csv(f"{csvname}.csv")

            url=f"https://www.imdb.com/search/title/?title_type=feature,tv_series&year=2023-01-01,2023-12-31&countries=IN&start={i}&explore=countries&ref_=adv_nxt"

            # Define the URL and retrieve data
            list2 = gettingdata(2023, url)

            # Create a DataFrame from 'list2'
            new_data = pd.DataFrame(list2, columns=["TTN","Name", "Duration", "Description", "year", "Genre", "director", "actors", "votes", "rating"])

            # Reset the index of the new data DataFrame
            new_data.reset_index(drop=True, inplace=True)

            # Reset the index of the existing DataFrame
            existing_df.reset_index(drop=True, inplace=True)

            # Concatenate the new data with the existing data
            combined_df = pd.concat([existing_df, new_data], ignore_index=True)

            # Write the combined DataFrame to a temporary CSV file
            combined_df.to_csv(f"temp_{csvname}.csv", index=False)

            # Rename the temporary CSV file to the original file name
            import os
            os.rename(f"temp_{csvname}.csv", f"{csvname}.csv")

        except Exception as e:
            print(f"Error: {e}")
            continue


def fetch(csv):
# First, call trip1 to create the initial CSV
    trip1(f'{csv}',firsturl)
    # Then, call resttrips to append data to the CSV
    #resttrips(f'{csv}', totalentries=recordsinimdb)

    #add index
    df = pd.read_csv(f'{csv}.csv')

    # Add an index column to the DataFrame
    df.insert(0, 'Index', range(1, len(df) + 1))

# Save the DataFrame with the added index back to a CSV file
    df.to_csv(f'{csv}.csv', index=False)




def main():

    start_time = time.time()
    #csv name
    fetch('z')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)


if __name__ == "__main__":
    main()