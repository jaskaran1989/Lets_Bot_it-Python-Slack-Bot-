import time
import urllib
import urllib.request as urllib2
from bs4 import BeautifulSoup
from google import search
from slackclient import SlackClient
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import config
import sys

bot_name = 'ninja'
bot_id = SlackClient(config.bot_id['BOT_ID'])
at_bot = "<@" + str(bot_id) + ">:"
slack_client = SlackClient(config.slack_token['SLACK_TOKEN'])


def parse_data(slack_data):
    inputdata = slack_data
    if inputdata and len(inputdata) > 0:
        for data in inputdata:
            if data and 'text' in data != bot_id:
                return data['text'], data['channel']
    return None, None


def chat(input_command, channel):
 
    so_url = "http://stackoverflow.com"
  
    if (input_command=="mergesort" ):
      
        url ="https://stackoverflow.com/questions/13727030/mergesort-in-java"
    
    if (input_command.lower()=="quicksort"):
        url ="https://stackoverflow.com/questions/14907334/stackoverflow-with-quicksort-java-implementation/14911816"

    if (input_command.lower()=="insertionsort"):
        url ="https://stackoverflow.com/questions/28379397/simple-insertion-sort"

    if (input_command.lower()=="heapsort"):
        url ="https://stackoverflow.com/questions/13979714/heap-sort-how-to-sort"

    if (input_command.lower()=="bubblesort"):
        url ="https://stackoverflow.com/questions/16088994/sorting-an-array-of-int-using-bubblesort"

    if (input_command.lower()=="BFS"):
        url ="https://stackoverflow.com/questions/2505431/breadth-first-search-and-depth-first-search"

    if (input_command.lower()=="DFS"):
        url ="https://stackoverflow.com/questions/21508765/how-to-implement-depth-first-search-for-graph-with-non-recursive-aprroach/21514860"

    


    if "http://stackoverflow.com/" or "http://stackoverflow.com/" in url:
        print(input_command)
        so_url = url
        slack_client.api_call("chat.postMessage", channel=channel, text=str(url), as_user=True)
    try:
        print(so_url)
        page = urllib2.urlopen(so_url)
        soup = BeautifulSoup(page.read(),"lxml")
        result = soup.find(attrs={'class': 'answer accepted-answer'})
        
        if result is not None:
            print("i AM HERE NOW2")
            res = result.find(attrs={'class': 'post-text'})
            for a in res:
                if a.string is None:
                    a.string = ' '
                    print("i AM HERE NOW3")
            slack_client.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```",
                                  as_user=True)
        sys.exit()
    except IndexError:
        
        page = urllib2.urlopen(so_url)
        soup = BeautifulSoup(page.read(),"lxml")
        print("i AM HERE NOW")
        result = soup.find(attrs={'class': 'answer'})
        if result is not None:
            res = result.find(attrs={'class': 'post-text'})
            for a in res:
                if a.string is None:
                    a.string = ' '
                    
            slack_client.api_call("chat.postMessage", channel=channel, text="```" + res.get_text() + "```",
                                  as_user=True)
                
        
    except:
        #print("Could not parse")
        #slack_client.api_call("chat.postMessage", channel=channel, text="Could not find a relevant link", as_user=True)
        raise




def ninjafy():
    if slack_client.rtm_connect():
        print("Connected")
        while True:
            input_command, channel = parse_data(slack_client.rtm_read())
            if input_command and channel:
                chat(input_command, channel)
            time.sleep(1)
            
    else:

        print("Connection failed")


if __name__ == '__main__':
    ninjafy()
