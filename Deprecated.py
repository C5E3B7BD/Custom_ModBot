import urllib3
import datetime
from Workers import Helpers

from bs4 import BeautifulSoup

global http
http = urllib3.PoolManager()
class Actors:
    def __init__(self):
        '''Nothing Goes on here'''
        
    def Age(self, min_birthYear_Date, max_birthYear_Date = str(datetime.date.today()), URL_additions = ''):
        #Features needing added:
        #Name Groups (awards)
        #an actual gender switch
        #Star sign (why does IMDB even have this?)
        Link ="http://www.imdb.com/search/name?birth_date="
        Link += str(min_birthYear_Date)+','
        Link += str(max_birthYear_Date)
        Link += URL_additions
        webPage = http.request('GET', Link)
        webPageData = webPage.data
        soup = BeautifulSoup(webPageData)
        ActorList = []
        for ActorObject in soup.findAll('td', {'class': 'name'}):
            aTagObject = ActorObject('a')
            aTag_ActorNameOnly = aTagObject[0]
            NamedActorObject = aTag_ActorNameOnly.decode_contents()
            if len(ActorList)<50:
                        ActorList.append(str(NamedActorObject))
        return ActorList
class Movies:
    def __init__(self):
        '''Nothing Goes on here'''
        
    def Plot(self, Terms, URL_additions=''):
        Link="http://www.imdb.com/search/text?realm=title&field=plot&q="
        Link+=Terms
        Link+=URL_additions
        webPage = http.request('GET', Link)
        webPageData = webPage.data
        soup = BeautifulSoup(webPageData)
        MoviesList = []
        for MovieObject in soup.findAll('td', {'class': 'title'}):
            aTagObject = MovieObject('a')
            aTag_MovieNameOnly = aTagObject[0]
            NamedMovieObject = aTag_MovieNameOnly.decode_contents()
            if len(MoviesList)<50:
                        MoviesList.append(str(NamedMovieObject))
        Helper = Helpers
        MoviesList = Helper.makeUnique(MoviesList)
        return MoviesList
    
    def Genre(self, Genre, URL_additions=''):
        Link = 'http://www.imdb.com/genre/'
        Link += Genre
        Link += URL_additions
        webPage = http.request('GET', Link)
        webPageData = webPage.data
        soup = BeautifulSoup(webPageData)
        MoviesList = []
        for MovieObject in soup.findAll('td', {'class': 'title'}):
            aTagObject = MovieObject('a')
            aTag_MovieNameOnly = aTagObject[0]
            NamedMovieObject = aTag_MovieNameOnly.decode_contents()
            if len(MoviesList)<50:
                        MoviesList.append(str(NamedMovieObject))
        Helper = Helpers
        MoviesList = Helper.makeUnique(MoviesList)
        return MoviesList
    
    def Keyword(self, Keyword, URL_additions=''):
        #this class also returns the "Episode" name for some reason
        Link = "http://www.imdb.com/keyword/"
        Link += Keyword.lower()
        Link += URL_additions
        webPage = http.request('GET', Link)
        webPageData = webPage.data
        soup = BeautifulSoup(webPageData)
        MoviesList = []
        for tdObj in soup.findAll('table', {'class': 'results'}):
            aObj = tdObj('a')
            for x in aObj:
                    y = x.decode_contents()
                    if not('img' in y):
                            if not(y==aObj[0].decode_contents()) and not(y==aObj[1].decode_contents()):
                                    MoviesList.append(str(y))
        Helper = Helpers
        MoviesList = Helper.makeUnique(MoviesList)
        return MoviesList
    
    def Title(self, movieTitle, URL_additions = ''):
        #TODO: add "actors, yearMadeMinimum, and yearMadeMaximum"
        Link = "http://www.imdb.com/find?q="
        Link += movieTitle
        Link += "&s=tt"
        Link += URL_additions
        webPage = http.request('GET', Link)
        webPageData = webPage.data
        soup = BeautifulSoup(webPageData)
        MoviesList = []
        for MovieObject in soup.findAll('td', {'class': 'result_text'}):
            aTagObject = MovieObject('a')
            aTag_MovieNameOnly = aTagObject[0]
            NamedMovieObject = aTag_MovieNameOnly.decode_contents()
            if len(MoviesList)<50:
                        MoviesList.append(str(NamedMovieObject))
        Helper = Helpers
        MoviesList = Helper.makeUnique(MoviesList)
        return MoviesList


    
