 
import urllib.request
import json 
import re 
import newspaper

import gspread 
from oauth2client.service_account import ServiceAccountCredentials

from TwitterSearch import *


#================================================================set up 
#================================================================ News 
#keywords 
r = re.compile(r'missing\b | cyber\b | audit\b | scam\b | fake\b | laundering\b | breach\b | corrupt\b', flags=re.I | re.X) 

#newspapers API 
newspapers = [
'https://newsapi.org/v1/articles?source=abc-news-au&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=financial-times&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=associated-press&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b',
'https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=google-news&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=newsweek&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=reddit-r-all&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b',
'https://newsapi.org/v1/articles?source=reuters&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=the-economist&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=the-guardian-au&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=the-wall-street-journal&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=time&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b', 
'https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=33cae01fecbb4319ab7f2ee6df41588b'
]





#====================================================================Google Sheet API 

#printing the results in Google Sheet 

client_secret = r'C:\Users\***\MyProject_perso.json'

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret , scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.



#====================================================================== articles mining and parsing 
def newsScrapy(): 
    sheet = client.open("NewsScrapy").sheet1
    #resize the sheet to append to the first blank row 
    sheet.resize(1)
    

    
    for n in newspapers: 
        URL = urllib.request.urlopen(n)
        data = URL.read()
        encoding = URL.info().get_content_charset('utf-8')
        JSON_object = json.loads(data.decode(encoding))
    
        art = JSON_object['articles']
                    
        for i in art:
            for x in i: 
                if(x == 'title'): 
                    s = i[x].lower() 
                    match = r.search(s)
                    if(match is not None):  
                        print(i[x])
                        print(i['url'])
                        report_sheet = [i[x] , i['url']]
                        sheet.append_row(report_sheet)
                    

#======================================================================== newspaper library\
                    
# =============================================================================
# def news_lib(website):
# 
#     paper = newspaper.build(website,memoize_articles=False )
#  
#     for article in paper.articles: 
#         article.download()
#         article.parse()    
#         s = (article.text).lower()
#         match = r.search(s) 
#         if(match is not None): 
#             article.download()
#             article.parse()
#             print(article.summary)
#             print(article.url)                         
#             report_sheet = [article.summary , article.url]
#             sheet.append_row(report_sheet)                   
#  
# 
# 
# =============================================================================
#=========================================================== social media 

def twitterScrapy(t): 
    sh = client.open("NewsScrapy")
    sheet_2 = sh.get_worksheet(1)
    
    
    #resize the sheet to append to the first blank row 
    sheet_2.resize(1) 
    
    
           
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['fraud'], or_operator = True)
        tso.set_keywords(['scam'], or_operator = True)
        tso.set_keywords(['breach'])
        
       
        
        tso.set_include_entities(False) # and don't give us all those entity information
                      
    
    
        ts = TwitterSearch(
                consumer_key = 'yP37M6fOvZS5yKtXXeScOthlj',
                consumer_secret = 'TD5XRVucXj32TxVzqEmm9PrLDcVINFV19rNj4v1PcgsOGyYCir',
                access_token = '1128873464-4uGGex5TkcZANMSZjtQe2t1tuWi023Sds2OyCiv',
                access_token_secret = '4Hxc6RWkA4IYmMVWPS6BEgtvcDPBi5yC0FForvPNvvcQ3')
    
     # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tso):          
            if int(tweet['retweet_count']) > t: 
                s = tweet['text']
                rt = re.compile(r'RT', flags=re.I | re.X) 
                match = rt.search(s)           
                if(match is None): 
                    print( tweet['user']['screen_name'], tweet['text'],tweet['retweet_count'] )
                    report_sheet = [tweet['user']['screen_name'], tweet['text'],tweet['retweet_count']]
                    sheet_2.append_row(report_sheet)
                    
    
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
     





        
        




