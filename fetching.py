import requests
from bs4 import BeautifulSoup


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
