# if you want to sort recomendation according to the ratings just provide api key at line 33 you can get it from here http://www.omdbapi.com/ 
import json
import requests

def get_movies_from_tastedive(moviename):
    p={}
    url="https://tastedive.com/api/similar"
    p["q"]=moviename
    p["type"]="movies"
    p["limit"]="5"
    jsonResponse=requests.get(url,params=p)
    response=jsonResponse.json()
    return response

def extract_movie_titles(data):
    sortedData=[movieInfo["Name"] for movieInfo in data["Similar"]["Results"]]
    return sortedData

    
def get_related_titles(movieList):
    relatedTitles=[]
    for movie in movieList:
        tastediveResponse=get_movies_from_tastedive(movie)
        filterResponse=extract_movie_titles(tastediveResponse)
        relatedTitles+=[relatedMovie for relatedMovie in filterResponse if relatedMovie not in relatedTitles]
    return relatedTitles

def get_movie_data(movieTitle):
    p={}
    url="http://www.omdbapi.com/"
    p["t"]=movieTitle
    p["r"]="json"
    jsonResponse=requests.get(url,params=p)
    print(jsonResponse.text)
    response=jsonResponse.json()
    return response

def get_movie_rating(response):
    rating=0
    print(response.keys())
    for ratingInfo in response["Ratings"]:
        if ratingInfo["Source"]=="Rotten Tomatoes":
            rating=ratingInfo["Value"]
    if type(rating)==str:
        rating=rating.replace("%","")   
    return int(rating)

def keyFunForSort(movie):
    rating=get_movie_rating(get_movie_data(movie))
    return (rating,movie)

def get_sorted_recommendations(listOfMovies):
    relatedMovies=get_related_titles(listOfMovies)
    print(relatedMovies)
    relatedMovies=sorted(relatedMovies,key=keyFunForSort,reverse=True)
    print(relatedMovies)
    return relatedMovies

lst=[]    
while True:
    lst+=[input("Enter the movie to get recomedation from:\n")]
    answer=input("Do you want to enter More? Y/N\n")
    if answer=='n' or answer=='N':
        break

print('HERE ARE THE RECOMENDATIONS ACCORDING TO THEIR RATINGS')
print('Loading..\n')
print(get_sorted_recommendations(lst))