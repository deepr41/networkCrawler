import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np
import logging
import time
from os import path,mkdir,fsync

from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
userAgentList = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


class WebSpider(scrapy.Spider):
    #start_urls = ['https://www.google.com/']

    def __init__(self, name, urls, web_info):#data = 'data.csv', errorFile = 'fetchError.csv',finale = 'finale.csv'):
        self.name = name
        self.start_urls = urls
        self.web_info = web_info
        print('start_urls',self.start_urls)
        print('web_info',self.web_info)
        # # self.start_urls=url
        # self.errorFile = open(errorFile,'w')
        # self.finale = open(finale,'w')
        # # data = pd.read_csv(data)
        # # data = data.replace(np.nan, '', regex=True)
        # self.start_urls = []
        # self.web_info = []
        # k = pd.read_csv('top-1m-websites.csv')
        # self.webdict={}
        # for i,row in k.head(15).iterrows():
        #     self.webdict[row['slno']] = row['websiteName']
        # for i,row in data.head(15).iterrows():
        #     self.start_urls.append('https://www.'+self.webdict[row['slno']])
        #     self.web_info.append(row.tolist())
        # print('start_urls',self.start_urls)
        # print('web_info',self.web_info)
        
    # def __init__(self,name, url, slno, aliasString, errorFile = 'fetchError.csv',finale = 'finale.csv'):
    #     logging.getLogger('scrapy').setLevel(logging.ERROR)

    #     self.name = name
    #     self.slno = slno
    #     self.url = url[12:]
    #     self.start_urls=[url]
    #     #self.errorFile = open(errorFile,'a')
    #     #self.finale = open(finale,'a')
    #     self.aliasString = aliasString
    #     #self.logger = logging.getLogger("ErrorLogger")
        
    def start_requests(self):
        for u in self.start_urls:
            request = Request(u, callback=self.parse, errback=self.errback, dont_filter=True)
            request.meta['request_url'] = u
            yield request
    
    def parse(self, response):
        #print("*************************",response.url)
        titles = []
        descriptions = []
        language = []
        keywords=[]
        try:
            title1 = [title.extract() for title in response.xpath("//title/text()")]
            #print("title1: ",title1)
            titles.extend(title1)
        except:
            pass
        try:
            title2 = [title.extract() for title in response.xpath("//meta[@property='og:title']/@content")]
            #print("title2: ",title2)
            titles.extend(title2)
        except:
            pass
        try:
            title3 = [title.extract() for title in response.xpath("//meta[@property='twitter:title']/@content")]
            #print("title3: ",title3)
            titles.extend(title3)
        except:
            pass
        try:
            title4 = [title.extract() for title in response.xpath("//*[@name='title']/@content")]
            #print("title4: ",title4)
            titles.extend(title4)
        except:
            pass
        try:
            title5 = [title.extract() for title in response.xpath("//*[@name='og:title']/@content")]
            # print("title5: ",title5)
            titles.extend(title5)
        except:
            pass
        try:
            title6 = [title.extract() for title in response.xpath("//*[@name='twitter:title']/@content")]
            #print("title6: ",title6)
            titles.extend(title6)
        except:
            pass
        try:
            desc1 = [desc.extract() for desc in response.xpath("//meta[@name='og:description']/@content")]
            descriptions.extend(desc1)
        except:
            pass
        try:
            desc2 = [desc.extract() for desc in response.xpath("//meta[@name='twitter:description']/@content")]
            descriptions.extend(desc2)
        except:
            pass
        try:
            desc3 = [desc.extract() for desc in response.xpath("//*[@name='description']/@content")]
            descrptions.extend(desc3)
        except:
            pass
        try:
            desc4 = [desc.extract() for desc in response.xpath("//meta[@property='og:description']/@content")]
            descriptions.extend(desc4)
        except:
            pass
        try:
            desc5 = [desc.extract() for desc in response.xpath("//meta[@property='twitter:description']/@content")]
            descriptions.extend(desc5)
        except:
            pass
        
        try:
            lang1 = [lang.extract() for lang in response.xpath("//*[@http-equiv='content-language']/@content")]
            language.extend(lang1)
        except:
            pass
        try:
            lang2 = [lang.extract() for lang in response.xpath("//*/@lang")]
            language.extend(lang2)
        except:
            pass
        try:
            keywords.extend([keyword.extract() for keyword in response.xpath("//meta[@name='keywords']/@content")])#.replace(',',' ').replace('\n',' ')
        except:
            pass
        titles = list(i.replace(',',' ').replace("\n"," ").replace("\r",' ') for i in titles)
        descriptions = list(i.replace(',',' ').replace("\n"," ").replace("\r",' ') for i in descriptions)
        language = list(i.replace(',',' ').replace("\n"," ").replace("\r",' ') for i in language)
        keywords = list(i.replace(',',' ').replace("\n"," ").replace("\r",' ') for i in keywords)
        # print('\n\n *******************************\n',titles,'\n\n')
        # print('\n\n *******************************\n',descriptions,'\n\n')
        # print('\n\n *******************************\n',language,'\n\n')
        # print('\n\n *******************************\n',keywords,'\n\n')

        titlesString = ''
        for j in titles:
            titlesString = titlesString + ' ' + j
        titlesString = titlesString.strip()

        descString = ''
        for j in descriptions:
            descString = descString + ' ' + j
        descString = descString.strip()

        langString = ''
        for j in language:
            langString = langString + ' ' + j
        langString = langString.strip()

        keyString = ''
        for j in keywords:
            langString = keyString + ' ' + j
        keyString = keyString.strip()
        
        
        url = response.meta['request_url']
        aliasString = ''
        urlIndex = self.start_urls.index(url)
        slno = self.web_info[urlIndex][0]
        for j in self.web_info[urlIndex]:
            aliasString = aliasString + str(j) + ','
        
        finalString = aliasString+titlesString+','+descString+','+langString+','+keyString
        finale.write(finalString+'\n')
        # finale.flush()
        # fsync(finale.fileno())
        
        # slno = self.web_info[urlIndex][0]
        # url = self.webdict[slno]
        try:
            websiteData = response.text
            # if not (path.exists('./WebPages 2')):
            #     mkdir('./WebPages 2')
            with open('./WebPages 2/'+str(slno)+'_'+url[8:]+'.html','w') as webPageFile:
                webPageFile.write(websiteData)
        except Exception as e:
            print(slno," FAIL - ",e)
        
        #print('\n\n *******************************\n',self.aliasString+','+titlesString+','+descString+','+langString+','+keyString,'\n\n')
        print(slno," PASS",url)

    def errback(self, failure):
        e = 'Error '
        try:
            url = failure.value.response.meta['request_url']
            slno = self.web_info[self.start_urls.index(url)][0]
        except:
            request = failure.request
            url = request.meta['request_url']
            slno = self.web_info[self.start_urls.index(url)][0]
            print(slno," FAIL",url)
        
        if failure.check(HttpError):
            logging.log(logging.ERROR,'HttpError on '+ url)
            e = e+'HttpError'

        elif failure.check(DNSLookupError):
            logging.log(logging.ERROR,'DNSLookupError on '+ url)
            e = e+'DNSLookupError'

        elif failure.check(TimeoutError, TCPTimedOutError):
            logging.log(logging.ERROR,'TimeoutError on '+ url)
            e = e+'TimeoutError'
        else:
            logging.log(logging.ERROR,repr(failure))
        
        failString = ''
        for j in self.web_info[self.start_urls.index(url)]:
            failString = failString + str(j) + ','
        
        errorFile.write(failString+e+'\n')
        # errorFile.flush()
        # fsync(errorFile.fileno())

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'#'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',

})


# df = pd.read_csv('data.csv')
# finale = open('finalfile.csv',w)

# start = int(input("Enter starting sample number : "))
# num_samples = int(input("Enter number of samples to scrape : "))

# df = pd.read_csv('data.csv')
# data = df.replace(np.nan, '', regex=True)
# k = pd.read_csv('top-1m-websites.csv')
# webdict={}
# for i,row in k.head(2000).iterrows():
#     webdict[row['slno']] = row['websiteName']

# inittime1 = time.time()
# for i,row in data[start:start+num_samples].iterrows():
#     url='https://www.'+webdict[row['slno']]
#     aliasString = str(row[0])+','+str(row[1])+','+str(row[2])+','+str(row[3])
#     process.crawl(WebSpider,row['slno'], url, row['slno'], aliasString)
# inittime2 = time.time()
# print("Spiders initialised - ",inittime2-inittime1)

# proctime=time.time()
# errorFile = open('fetchError.csv','a')
# finale = open('finale.csv','a')
# process.start()
# print("Total time taken : ",time.time()-proctime)

start = int(input("Enter starting sample number : "))
num_samples = int(input("Enter number of samples to scrape : "))
num_spiders = int(input("Enter number of spiders : "))

df = pd.read_csv('dataMerged.csv')
data = df.replace(np.nan, '', regex=True)
startIndex = start
for j in range(1,num_spiders+1):
    endIndex = int(startIndex+num_samples/num_spiders) 
    
    start_urls = []
    web_info = []

    for i,row in data.iloc[startIndex:endIndex,].iterrows():
        start_urls.append('https://www.'+row['websiteName'])
        web_info.append(row.tolist())
    process.crawl(WebSpider,name = j, urls = start_urls, web_info = web_info)
    startIndex = endIndex

errorFile = open('fetchError.csv','a')
finale = open('finale.csv','a')

start_time = time.time()
try:
    process.start()
    process.join()
except Exception as e:
    print("Process failed error: ",e)
print("Total time : ",time.time()-start_time)