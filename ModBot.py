import praw
import configparser
import time
import pprint
import urllib3
import datetime
from IMDbParser import IMDbParser
from bs4 import BeautifulSoup
r = praw.Reddit('Customized modbot for scottss by /u/subconcussive')
q = IMDbParser.Actor()

#Parse settings.config
config = configparser.ConfigParser()
config.read('settings.cfg')

#Get the Username, Password, and Subreddit
#With error handling
#-----------------------------------------#
try:
    username = config.get('AUTH', 'USERNAME')
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        username = dargs[0]
    except:
        username = input("Enter Username: ")
        if username == '':
            raise ValueError()
try:
    password = config.get('AUTH', 'PASSWORD')
    if password == '':
        raise ValueError()
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        password = dargs[1]
    except:
        password = input("Enter Password: ")
        if password == '':
            raise ValueError()
try:
    subR = config.get('SETTINGS', 'SUBREDDIT')
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        subR = dargs[2]
    except:
        subR = input("Enter Subreddit: ")
        if subR == '':
            raise ValueError()
#-----------------------------------------#

#Assign seperators
#-----------------------------------------#
print('\n\n\n')
topSep = '|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|'
bottomSep = '|=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=|'
#-----------------------------------------#


#Now login
#-----------------------------------------#
print('%s\n|Ignore any warnings that pop up                  |'% topSep)
print("|They don't affect the bot.                       |")
r.login(username, password)
print('%s\n'% bottomSep)
#-----------------------------------------#

#Now do some setting up
#-----------------------------------------#
already_done = []
finished = False
starletNames = []
flaggedFor=""
miscVar = 0
todayDate = None
alreadyMadeAThreadThisMonth = False
otherDate = datetime.date.today()
#-----------------------------------------#

#Main Loop
#This one never exits
#-----------------------------------------#
while True:              
    subreddit = r.get_subreddit(subR)
    numlimit = 15
    smsn=subreddit.get_new(limit=numlimit)
    finished = False #Finished is set to true if/when we run into a submission that's contained in "already_done[]"

    #Request thread logic
    if datetime.date.today().day == 1:
        if not alreadyMadeAThreadThisMonth:
            uSubmissions = r.get_redditor(username).get_submitted()
            threadString = str(datetime.datetime.now().strftime("%B")) + " " + str(datetime.date.today().year) + " Request Thread."
            threadText = "Remember, please post your celebrity requests here as a comment, **ONE NAME ONLY PER REQUEST**, so that each name can be voted on separately.\n\n**HEADSHOTS (HS) MUST BE PHOTOS TAKEN OF CELEBRITIES AFTER HAVING ALREADY TURNED 18**. \n\nIt is not okay to put a 15-year old's head on an 18-year old's body.\n\nNot here, at least.\n\nHere, that will get you immediately and permanently banned from this subreddit.\n\nThank you for your cooperation."
            for sM in uSubmissions:
                if sM.title == threadString:
                    alreadyMadeAThreadThisMonth = True
                else:
                    requestSubmission = subreddit.submit(threadString, threadText)
                    if not requestSubmission.stickied:
                        if subreddit.reddit_session.user.is_mod:
                            requestSubmission.sticky
                    uS = r.get_redditor(username).get_submitted()
                    '''submissionArray = []
                    for userSubmission in uS:
                        submissionArray.append(userSubmission)
                    requestSubmission = submissionArray[0]
                    if not requestSubmission.stickied:
                        if subreddit.reddit_session.user.is_mod:
                            requestSubmission.sticky'''
    while not finished:
        todayDate = datetime.date.today()
        
        min_birthYear = str(todayDate.year-18)+"-"
        if todayDate.month < 10:
            min_birthYear += "0"+str(todayDate.month)+"-"+str(todayDate.day)
        else:
            min_birthYear += str(todayDate.month)+"-"+str(todayDate.day)
        max_birthYear = str(todayDate)
        additions = '&gender=female'
        
        IMDbLink = "http://www.imdb.com/search/name?birth_date=" + str(min_birthYear) + ',' + str(max_birthYear) + additions
        if todayDate != otherDate:
            starletNames = q.Age(min_birthYear,max_birthYear,additions)
            otherDate = datetime.date.today()
        for submission in smsn:            
            if (submission.id in already_done):
                finished = True
            else:
                spacerThing = ""
                for i in range(1, int(50-len(submission.title))):
                    spacerThing +=" "
                if len(submission.title)>49:
                    print(('\n%s\n|'+submission.title[:45]+'... '+'|')% topSep)
                else:
                    print(('\n%s\n|'+submission.title+spacerThing+'|')% topSep)
                flaggedFor=""
                test = '%s'% submission.title
                test = test.lower()
                for star in starletNames:
                    if (star.lower() in test):
                        if len(flaggedFor)>0:
                            flaggedFor += ", "
                        flaggedFor += star
                comment = config.get('RESOURCES', 'COMMENT')#% IMDbLink, star
                comment = comment.replace("\\n","\n")
                comment = comment.format(IMDbLink, flaggedFor)
                submission.replace_more_comments()
                if not submission.comments:
                    print("|No comments                                      |")
                else:
                    spacerThing = ""
                    for i in range(10, int(50-len(str(len(submission.comments))))):
                        spacerThing += " "
                    if len(submission.comments)>1:
                        print("|"+str(len(submission.comments))+" comments"+spacerThing+'|')
                    else:
                        print("|"+str(len(submission.comments))+" comment "+spacerThing+'|')                    

                testCaseThing = (submission.id not in already_done) and (flaggedFor != '')
                #Check if the user has already commented in this thread, if so don't comment
                #-----------------------------------------#
                for commentitem in submission.comments:
                    try:
                        boolThing = (username==commentitem.author.name)
                        if (boolThing):
                            print("|One of my comments                               |")
                            print("|I've already commented in this thread            |")
                            testCaseThing = False
                        else:
                            miscVar+=1
                    except AttributeError:
                        miscVar+=1
                        #Someone Deleted this comment, I don't know if it was me
                #-----------------------------------------#
                #        
                #Test if the user has already done this submission, and that it's actually flagged for something
                #Check if the user is a moderator in that subreddit, if so distinguish the comment
                #Report the comment
                #-----------------------------------------#
                if testCaseThing == True:
                    if subreddit.reddit_session.user.is_mod:
                        submission.distinguish()
                    submission.report()
                    submission.add_comment(comment)
                    print("|Commented                                        |")
                    print(bottomSep)
                else:
                    print("|Not commenting in this thread                    |")
                    already_done.append(submission.id)
                    print(bottomSep)
                already_done.append(submission.id)
                time.sleep(1)
                #-----------------------------------------#
            already_done.append(submission.id)
            time.sleep(2)
        if (submission.id in already_done):
            finished = True
    try:
        already_done.append(submission.id)
    except:
        shouldnt_Ever_Happen = []
    time.sleep(30)
                
                
                
        
                                        
