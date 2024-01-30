from pprint import pprint

import requests
from bs4 import BeautifulSoup

#headers- to handle 403(forbidden error) - f12 in chrome-reload page - network tab-html-user agent
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0.0.0 Safari/537.36"}

response = requests.get('https://www.imdb.com/find/?s=ep&q=thriller&ref_=nv_sr_sm',
                        headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
result_list = []

#get all names of the TV shows with name thriller
movies_list = soup.find('div',{'class':'sc-17bafbdb-2 iUyFfD'})
movie = movies_list.findAll('li')
for movie in movie:
    movie_section = movie.find('div',{'class':'ipc-metadata-list-summary-item__c'})
    #retrieve data if movie name exists
    if movie_section:
        movie_genre_dict = {}
        # class name given in curly braces will uniquely identify the div
        movie_div = movie_section.find('div',{'class':'ipc-metadata-list-summary-item__tc'})
        #to get movie name
        movie_name = movie_div.find('a').getText()
        movie_genre_dict['movie'] = movie_name
        #to get the genre of the movie from child page
        child_page_link = movie_div.find('a').get('href')
        #print(child_page_link)
        child_page = requests.get('https://www.imdb.com'+child_page_link, headers=headers)
        child_soup = BeautifulSoup(child_page.text, 'html.parser')
        child_div = child_soup.find('div',{'class':'ipc-chip-list__scroller'})
        if child_div:
            genre_list = child_div.findAll('a')
            genre_data = []
            # to get list of genre
            for genre in genre_list:
                genre_name = genre.find('span').getText()
                genre_data.append(genre_name)
                movie_genre_dict['genre'] = genre_data
    # if genre exists then appending list with movies in genre-music
    if movie_genre_dict.get("genre") and 'Music' in movie_genre_dict.get("genre"):
        result_list.append(movie_genre_dict)

pprint(result_list)

