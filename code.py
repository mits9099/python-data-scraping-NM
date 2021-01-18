from tweepy import OAuthHandler #Handling authentication
import json #For writing to a JSON file
from pymongo import MongoClient
import tweepy
#from matplotlib import pyplot
from nltk.tokenize import word_tokenize
import re
#import jsonpickle
import time
# Twitter developer app
access_token = '2897284776-zup0PRNQz3oZq0MyA9A8nkCU5jfgERELFQ4hty4'
access_token_secret = 'eFwK7rIpKP5KsMPLOsUU4S6Kr7wM28cTQleCr0hEr29EO'
consumer_token = 'BvzQwQ8fWQsVfanO3lYHaIord'
consumer_token_secret = 'Bej8fH5HfqYJl5YOJw7fRVTaiQKsr3fP2dQaddoVSgVB3FQ4LY'
#Mongodb connection
#client = MongoClient('localhost',27017)
#database = client['analysisNM']
#collection1 = database['weet']


fp=open("positive_essay.json",)
fn=open("negative_eassy.json",)
#f1=open("mitul.json","a")
possitive=json.load(fp)
negetive=json.load(fn)
n=1000#AS DEMO
l=n/1.5
tweetslist=[]
positivenumbtweets=0
addtopossitive=int(0+l)
addtoneutral=int(0-l)
addtonegative=0
testers=0




searchQuery = 'Narendra Modi'  
sinceId = None




def cleantext(txt):
    tweetsword = re.sub('[^a-zA-Z0-9\n]', ' ', txt)
    return tweetsword
def lowercasetext(txt):
    tlow=txt.lower()
    return tlow
def timerstart():
    starting=time.time()
    return starting
def timerend():
    ending=time.time()
    return ending
def timercal(ini,stopp):
    return (stopp-ini)
def dataprocess():  #function listen to fetch data from twitter
    #try:
    weetunt = 0
    upper_id = -1
    global testers


    stime = timerstart()
    
    #with open('Education.json', 'w') as f:
    while weetunt < n:
        try:
            if (upper_id <= 0):
                if (not sinceId):
                    tweets = api.search(q=searchQuery, lang='en')
                else:
                    tweets = api.search(q=searchQuery, since_id=sinceId)
            for weet in tweets:
                #ram=(jsonpickle.encode(weet._json, unpicklable=False) +'\n')
                singleweet= weet._json["text"]
                onedata = {"tweet":weet._json["text"]}
                #collection1.insert_one(onedata)
                print (singleweet)
                #print(weet._json)
                tweetswords= cleantext(singleweet)
                textlow= lowercasetext(tweetswords)
                
            #print(len(tweets))
            
            weetunt =weetunt+1 
            upper_id = tweets[-1].id
            tweetslist.append(textlow)
            
            testers=testers+1
            print(testers)
                
        except tweepy.TweepError:
            continue
    etime = timerend()
    actual_time=timercal(stime,etime)
    print ("Twitter data fetching time: {:.3f} sec".format(actual_time))

def tf(cleantweets):
    stime = timerstart()
    for singletweet in cleantweets:
        #print(singletweet)
        fwordz=word_tokenize(singletweet)
        #print(fwordz)
        for word in fwordz:
            if word in possitive :
                possitive[word]=possitive[word]+1
                #val.append(di[feq])
            else:
                continue
            for words in fwordz:
                if word in negetive :
                    negetive[words]=negetive[words]+1
                else:
                    continue
        collectnumbp = positivecount(possitive)
        collectnumbn = negativecount(negetive)
 
        sentimental(collectnumbp,collectnumbn)
    etime = timerend()
    actual_time=timercal(stime,etime)
    print ("sentimental data time: {:.3f} sec".format(actual_time))
    
def positivecount(positivedict):
    numb1=0
    counting = positivedict.values()
    #print(counting)
    for addi in counting:
        numb1=numb1+addi
    return numb1

def negativecount(negativedict):
    numb1=0
    counting = negativedict.values()
    for subi in counting:
        numb1=numb1+subi
    return numb1
def sentimental(posi,negi):
    global addtopossitive,addtonegative,addtoneutral
    #global addtonegative
    #global addtoneutral
    if (posi-negi>0):
        addtopossitive=addtopossitive+1
    elif(posi-negi<0):
        addtonegative=addtonegative+1
    else:
        addtoneutral=addtoneutral+1
        
 
if __name__ == "__main__":
    authentication = OAuthHandler(consumer_token,consumer_token_secret)#authentication handling
    authentication.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    dataprocess()
	#calling function dataprocess
    tf (tweetslist)
    rom = pyplot.figure()
    x = rom.add_axes([0,0,1,1])
    disgraph = ['Possitive', 'Neutral', 'Negative']
    inpgraph = [addtopossitive,addtoneutral,addtonegative]
    x.bar(disgraph, inpgraph)
    print("Positive tweets = {0}\nNeutral tweets = {1}\nNegative tweets = {2}".format(addtopossitive,addtoneutral,addtonegative))
    print("Percentage of positive tweets: {0:.2f}%\nPercentage of neutral tweets: {1:.2f}%\nPercentage of negative tweets: {2:.2f}%".format(((addtopossitive/n)*100),((addtoneutral/n)*100),((addtonegative/n)*100)))  
    pyplot.show()
    fp.close()
    fn.close()
