import fetching
import pandas as pd

def tripone(csvname,firsturl,release):
    url = firsturl
    finalist = fetching.gettingdata(release, url)
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
            list2 = fetching.gettingdata(2023, url)

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
