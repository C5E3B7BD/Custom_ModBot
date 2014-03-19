import urllib3
from Workers import Helpers
from bs4 import BeautifulSoup

global http
http = urllib3.PoolManager()
class Movies:
    def __init__(self):
        '''Nothing Goes on here'''
        
    def _Plot_(self, Terms, URL_additions=''):
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
    
    def _Genre_(self, Genre, URL_additions=''):
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
    
    def _Keyword_(self, Keyword, URL_additions=''):
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
    
    def _Title_(self, movieTitle, URL_additions = ''):
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
