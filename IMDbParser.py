import datetime
import _ActorsHandlers_
import _MoviesHandlers_
class Actor:
    def __init__(self):
        '''Null'''
    def Age(self, min_birthYear_Date, max_birthYear_Date = str(datetime.date.today()), URL_additions = ''):
        Handler = _ActorsHandlers_.Actors()._Age_(min_birthYear_Date, max_birthYear_Date, URL_additions)
        return Handler
class Movie:
    def __init__(self):
        '''Null'''
    def Plot(self, Terms, URL_additions=''):
        Handler = _MoviesHandlers_.Movies()._Plot_(Terms, URL_additions)
        return Handler    
    def Genre(self, Genre, URL_additions=''):
        Handler = _MoviesHandlers_.Movies()._Genre_(Genre, URL_additions)
        return Handler
    def Keyword(self, Keyword, URL_additions=''):
        Handler = _MoviesHandlers_.Movies()._Keyword_(Keyword, URL_additions)
        return Handler
    def Title(self, movieTitle, URL_additions = ''):
        Handler = _MoviesHandlers_.Movies()._Title_(movieTitle, URL_additions)
        return Handler
