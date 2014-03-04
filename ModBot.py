import praw
import configparser
import time
import pprint
import urllib3
import datetime
import IMDbParser
from bs4 import BeautifulSoup
r = praw.Reddit('Customized modbot for scottss by /u/subconcussive')
q = IMDbParser.Actors()

#Parse settings.config
config = configparser.ConfigParser()
config.read('settings.cfg')
username = config.get('auth', 'username')
password = config.get('auth', 'password')

#Now login
r.login(username, password)
print("\n\nIf you see a Deprecation warning please ignore it.\nPraw isn't caught up with the current version of Python yet\n\n\n")


#Now do some setting up
already_done = []
finished = False
starletNames = []

flaggedFor=""



#Main Loop
while True:
    subreddit = r.get_subreddit(config.get('settings', 'subreddit'))
    
    numlimit = 25
    smsn=subreddit.get_new(limit=numlimit)

    http = urllib3.PoolManager()
    
    while finished != True:



        min_birthYear = str(datetime.date(datetime.date.today().year-18,datetime.date.today().month,datetime.date.today().day))
        max_birthYear = str(datetime.date.today())
        additions = '&gender=female'

        
        IMDbLink = "http://www.imdb.com/search/name?birth_date="
        IMDbLink += str(min_birthYear)+','
        IMDbLink += str(max_birthYear)
        #That thing that looks like the Unicode unfound symbol box is just two _'s
        #IMDbLink += str('&start='+int(((page-1)*50)+1))
        IMDbLink += additions

        starletNames = q.GetListByAge(min_birthYear,max_birthYear,additions)
        for submission in smsn:
            print('\n'+submission.title+'\n=-=-=-=-=')
            flaggedFor=""            
            if (submission.id in already_done):
                finished = True
                break
            else:
                test = '%s'% submission.title
                test = test.lower()
                #testList = test1.split(' ')
                

                for star in starletNames:
                    if (star.lower() in test):
                        nameThing ='------------------------\n  Found a name match:\n'
                        i = 0
                        while (i < ((len('------------------------')-len(star))/2)):
                             nameThing+=' '
                             i+=1
                        nameThing += star+'\n------------------------'
                        if len(flaggedFor)>0:
                            flaggedFor += ", "
                        flaggedFor += star
                        

                #set the 'comment' variable
                comment = ("This post has been flagged as violating the rules of this subreddit. One of the names in your submission's title matched a name on a [list of underage actresses]({0}).\n\nThe name(s) matched are/is:\n\n    {1}\n\n^^^This ^^^is ^^^an ^^^automated ^^^response ^^^by ^^^a ^^^bot. ^^^If ^^^you ^^^believe ^^^that ^^^this ^^^submission ^^^was ^^^flagged ^^^in ^^^error ^^^please ^^^report ^^^this ^^^to ^^^the ^^^moderators ^^^of ^^^this ^^^subreddit ^^^or ^^^to ^^^my ^^^human: ^^^/u/subconcussive.")#% IMDbLink, star
                comment = comment.format(IMDbLink, flaggedFor)
                
                submission.replace_more_comments()
                if not submission.comments:
                    print("no comments")
                    
                testCaseThing = (submission.id not in already_done) and (flaggedFor != '')
                
                for commentitem in submission.comments:
                    try:
                        print(commentitem)
                        boolThing = (username==commentitem.author.name)
                        if (boolThing):
                            print("One of my comments\nI've already commented in this thread")
                            testCaseThing = False
                        else:
                            print("Not one of my comments")
                    except AttributeError:
                        print("Someone Deleted this comment, I don't know if it was me")
                
                if testCaseThing == True:
                    if subreddit.reddit_session.user.is_mod:
                        submission.report
                        submission.distinguish
                    submission.add_comment(comment)
                    print("Commented\n\n")
                else:
                    print("Not commenting in this thread")
                    already_done.append(submission.id)
                already_done.append(submission.id)
                time.sleep(2)
            time.sleep(3)
    time.sleep(5)
            
                
                
                
                
        
                                        
