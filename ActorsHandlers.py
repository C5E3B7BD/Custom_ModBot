import urllib3
import datetime
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
