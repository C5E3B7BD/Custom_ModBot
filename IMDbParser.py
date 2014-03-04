import urllib3
import datetime
from bs4 import BeautifulSoup

class Actors:
    global http
    http = urllib3.PoolManager()
    def __init__(self):
        global http
        http = urllib3.PoolManager()
        print ("init") # never prints
    def GetListByAge(self, min_birthYear_Date, max_birthYear_Date, URL_additions):
        IMDbLink ="http://www.imdb.com/search/name?birth_date="
        IMDbLink += str(min_birthYear_Date)+','
        IMDbLink += str(max_birthYear_Date)
#That thing that looks like the Unicode unfound symbol box is just two _'s
        #IMDbLink += str('&start='+int(((page-1)*50)+1))
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









'''
        class x:
            def login(self, username=None, password=None):
                    print("Good\n")
                    if username != None:
                            print("Good\n")
                            print(username)
                    else:
                            print("Username is blank\n")
                    if password != None:
                            print("Good\n")
                            print(password)
                    else:
                            print("Password is blank\n")
        r = x()
        r.login()
'''

'''
while counter < 2:
    while True:
        subreddit = r.get_subreddit(config.get('settings', 'subreddit'))
        numlimit = 5
        smsn=subreddit.get_new(limit=numlimit)
        for submission in smsn:
            if submission.id in done:
                counter+=1
                break
            else:
                for star in starletNames:
                    print(" "+str(star.lower() in test)+" ")
                print("\n======\n")
                done.append(submission.id)
'''
'''
for l in range(1):
    done=[]
    counter=1
    while counter < 2:
        subreddit = r.get_subreddit(config.get('settings', 'subreddit'))
        numlimit = 5
        smsn=subreddit.get_new(limit=numlimit)
        for submission in smsn:
                if submission.id in done:
                        counter+=1
                        break
                else:
                        for star in starletNames:
                                if(star.lower() in str(submission.title).lower()):
                                        print(str(submission.title))
                        print("\n======\n")
                        done.append(submission.id)
'''
