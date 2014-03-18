import urllib3
import datetime

from bs4 import BeautifulSoup

global http
http = urllib3.PoolManager()
class Actors:
    '''global http
    http = urllib3.PoolManager()'''
    def __init__(self):
        '''global http
        http = urllib3.PoolManager()'''
        #print ("init") # never prints
    def Age(self, min_birthYear_Date, max_birthYear_Date = str(datetime.date.today()), URL_additions = ''):
        #Features needing added:
        #Name Groups (awards)
        #an actual gender switch
        #Star sign (why does IMDB even have this?
        IMDbLink ="http://www.imdb.com/search/name?birth_date="
        IMDbLink += str(min_birthYear_Date)+','
        IMDbLink += str(max_birthYear_Date)
        IMDbLink += URL_additions
        webPage = http.request('GET',IMDbLink)
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
        global http
        http = urllib3.PoolManager()
    def Plot(self, Terms, URL_additions=''):
        IMDbLink="http://www.imdb.com/search/text?realm=title&field=plot&q="
        IMDbLink+=Terms
        IMDbLink+=URL_additions
        webPage = http.request('GET',IMDbLink)
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
        IMDbLink = 'http://www.imdb.com/genre/'
        IMDbLink += Genre
        IMDbLink += URL_additions
        webPage = http.request('GET',IMDbLink)
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
        IMDbLink = "http://www.imdb.com/keyword/"
        IMDbLink += Keyword.lower()
        IMDbLink += URL_additions
        #print(IMDbLink)
        webPage = http.request('GET',IMDbLink)
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
        '''for MovieObject in soup.findAll('td', {'class': 'title'}):
            aTagObject = MovieObject('a')
            aTag_MovieNameOnly = aTagObject[0]
            NamedMovieObject = aTag_MovieNameOnly.decode_contents()
            if len(MoviesList)<50:
                        MoviesList.append(str(NamedMovieObject))
        '''
        Helper = Helpers
        MoviesList = Helper.makeUnique(MoviesList)
        return MoviesList
    def Title(self, movieTitle, URL_additions = ''):
        #TODO: add "actors, yearMadeMinimum, and yearMadeMaximum"
        IMDbLink = "http://www.imdb.com/find?q="
        IMDbLink += movieTitle
        IMDbLink += "&s=tt"
        IMDbLink += URL_additions
        webPage = http.request('GET',IMDbLink)
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
    
'''
Now on to helper objects
TODO:
Move this to a seperate file
'''
class Helpers:
    def __init__(self):
        #null
        x=[]
    def makeUnique(seq, idfun=None):
       #Credit for this function goes to Peter Bengtsson
       #http://www.peterbe.com/
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result


    
