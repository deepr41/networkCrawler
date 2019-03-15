import socket
import pandas as pd
import numpy as np
import urllib
import time
import random
import traceback
from os import path,mkdir,fsync
from bs4 import BeautifulSoup
import sys
import re
import threading
import queue

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

def openFiles():
    from os import path
    if(path.exists('./networkData.csv')):
        finalFile = open('networkData.csv','a')
    else:
        finalFile = open('networkData.csv','a')
        finalFile.write("slno,hostname,alias,ipaddress\n")# ,titles,description,language,keyword\n")

    if(path.exists('./aliasError.csv')):
        aliasFile = open('aliasError.csv','a')
    else:
        aliasFile = open('aliasError.csv','a')
        aliasFile.write("slno,hostname\n")

    if(path.exists('./fetchError.csv')):
        fetchFile = open('fetchError.csv','a')
    else:
        fetchFile = open('fetchError.csv','a')
        fetchFile.write("slno,hostname\n")

    if not (path.exists('./WebPages')):
        mkdir('./WebPages')
    return (finalFile,aliasFile,fetchFile)

def readData(path): 
    try:
        return pd.read_csv('./top-1m-websites.csv',)
    except:
        print("Error in reading input file")

num_threads=50
q = queue.Queue(num_threads*3)
fullCondition = threading.Condition()
emptyCondition = threading.Condition()
queueCondition = threading.Condition()
finished=False

dataLock=threading.Lock()
fetchLock=threading.Lock()
aliasLock=threading.Lock()
class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, path='./top-1m-websites.csv', begin=None, num_samples=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name
        self.path=path
        if begin is None or num_samples is None:
            raise ValueError("Invalid Limits")
        self.begin=begin
        self.num_samples=num_samples

            

    def run(self):
        fileData = readData(path)
        i=self.begin
        global finished
        while i<self.begin+self.num_samples:
            if not q.full():
                url = str(fileData['websiteName'][i])
                slno = str(fileData['slno'][i])
                item=(slno,url)
                queueCondition.acquire()
                q.put(item)
                queueCondition.release()
                #emptyCondition.notify_all()
                #notifyall
                # print('Putting ' + str(item)  
                #               + ' : ' + str(q.qsize()) + ' items in queue')
                #time.sleep(random.random())
                i=i+1
            else:
                pass
                #fullCondition.wait()
        finished=True
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, files=None):
        super(ConsumerThread,self).__init__()
        if target is None:
            print("No target")
            exit()
        self.target = target
        self.name = name
        if files is None:
            print("No files")
            exit()
        self.files=files
        return

    def run(self):
        global finished
        while ((not finished) or (not q.empty())):
            if not q.empty():
                item = "queue is empty"
                queueCondition.acquire()
                if not q.empty():
                    item = q.get()
                else:
                    queueCondition.release()
                    time.sleep(1)
                    continue
                queueCondition.release()
                self.target(item,self.files)

                # print('Getting ' + str(item) 
                #               + ' : ' + str(q.qsize()) + ' items in queue')
            else:
                pass
                #fullCondition.notify()
                #emptyCondition.wait()

        return

def handleAliasError(err,aliasFile,slno,url):
    aliasLock.acquire()
    aliasFile.write(slno+','+url+'\n')
    aliasFile.flush()
    fsync(aliasFile.fileno()) 
    aliasLock.release() 
    # traceback.print_exc()

def handleFetchError(err,fetchFile,slno,url):
    fetchFile.write(slno+','+url+'\n')
    fetchFile.flush()
    fsync(fetchFile.fileno())   
    # traceback.print_exc()

def scrape(element,files):
    finalFile = files[0]
    aliasFile = files[1]
    fetchFile = files[2]
    slno=element[0]
    url=element[1]              
    #start=int(threading.current_thread().name)*int(total/num_threads)
    #end=start+int(total/num_threads)
    #for i in range(0,end - start):
    #print("Thread",threading.current_thread().name)
    #timeStart = time.time()
    #url = str(topTen['websiteName'][start + i])
    urltemp1 = 'www.'+ url
    #slno = str(topTen['slno'][start + i])
    try:
        hostData = socket.gethostbyname_ex(urltemp1)
        hostName = hostData[0]
        aliases = hostData[1]
        ipAddress= hostData[2]
        
        aliasString = ''
        for j in aliases:
            aliasString =aliasString +' ' +j
        aliasString = aliasString.strip()
        ipString = ''
        for j in ipAddress:
            ipString =ipString +' ' +j
        ipString = ipString.strip()
        # finalString = ''+slno+','+url+','+aliasString+','+ipString+'\n'
    except Exception as e:
        handleAliasError(e,aliasFile,slno,url)
        print('Failed :' + slno, end = "  ")
        #timeEnd = time.time()
        #print(timeEnd - timeStart)
        return
        #continue
    try:
        # urltemp2 = 'https://' + urltemp1
        # user_agent = random.choice(userAgentList)
        # request = urllib.request.Request(urltemp2, headers = {'User-Agent':user_agent})
        # response = urllib.request.urlopen(request, timeout= 20)
        # if(response.status != 200):
        #     raise Exception("Invalid Response")
        # response = requests.get(urltemp2)
        # soup = BeautifulSoup(response.read(), "html.parser")
        # websiteData = soup.prettify()
        # titlesString,descString,langString,keyword = getDetails(soup)
        # getDetails(soup)


        # finalString = ''+slno+','+hostName+','+aliasString+','+ipString+','+titlesString+','+descString+ \
                        # ','+langString+','+keyword+'\n'
        finalString = ''+slno+','+hostName+','+aliasString+','+ipString+'\n'
        dataLock.acquire()
        finalFile.write(finalString)
        finalFile.flush()
        fsync(finalFile.fileno())
        dataLock.release()
        print('Completed :' + slno, end = "\n")

        # with open('./WebPages/'+slno+'_'+url+'.html','w') as webPageFile:
        #     webPageFile.write(websiteData)
        # with open(slno+'_'+hostname+'.html')
        # break
    except Exception as e:
        handleFetchError(e,fetchFile,slno,url)
        print('Failed :' + slno, end = "  ")
    #timeEnd = time.time()
    #print(timeEnd - timeStart)
    #barrier.wait()
    #print("barrier passed at ",time.time()-timeProgramStart)

def main():
    files = openFiles()

    # # return
    # start,end = 0,20
    # total=end-start
    # csvData = readData(path)
    # topTen = csvData[start:end]
    
    begin=int(input("Enter starting : "))
    num_samples = int(input("Enter num samples : "))
    #timeProgramStart = time.time()
    
    #barrier=threading.Barrier(num_threads)
    startTime = time.time()
    barrier = threading.Barrier(num_threads)
    producer = ProducerThread(begin=begin,num_samples=num_samples)
    producer.start()
    consumerList = []
    for k in range(0,num_threads):
        consumer = ConsumerThread(name=str(k),target=scrape,files=files)
        consumerList.append(consumer)
        consumer.start()

    producer.join()
    for consumer in consumerList:
        consumer.join()
    endTime = time.time()
    print("Total time ",endTime-startTime)
    #timeProgramEnd = time.time()
    #print("Total time elapsed = ",timeProgramEnd - timeProgramStart)
    

def getDetails(soup):
    titles = []
    descps = []
    langs = []
    try:
        title1=soup.find('title').string
        #title1=title1.replace("<title>","")
        #titles.append(title1.replace("</title>",""))
        titles.append(title1)
    except:
        pass
    try:
        title2 = soup.find("meta",  property="og:title")
        titles.append(title2["content"] if title2 else None)
    except:
        pass
    try:
        title3 = soup.find("meta",  property="twitter:title")
        titles.append(title3["content"] if title3 else None)
    except:
        pass
    try:
        title4 = soup.findAll(attrs={"name": re.compile(r"title", re.I)})
        titles.append(title4[0]['content'] if title4 else None)
    except:
        pass
    try:
        desc1 = soup.find("meta",  property="og:description")
        descps.append(desc1["content"] if desc1 else None)
    except:
        pass
    try:
        desc2 = soup.find("meta",  property="twitter:description")
        descps.append(desc1["content"] if desc2 else None)
    except:
        pass
    try:
        desc3 = soup.findAll(attrs={"name": re.compile(r"description", re.I)})
        descps.append(desc3[0]['content']if desc3 else None)
    except:
        pass
    try:
        lang1 = soup.findAll(attrs={"http-equiv": re.compile(r"lang", re.I)})
        langs.append(lang1[0]['content']if lang1 else None)
    except:
        pass
    try:
        lang2 = soup.findAll(attrs={"name": re.compile(r"lang", re.I)})
        langs.append(lang2[0]['content']if lang2 else None)
    except:
        pass
    try:
        lang3 = soup.findAll(attrs={"lang": re.compile(r"lang", re.I)})
        langs.append(lang3[0]['content']if lang3 else None)
    except:
        pass
    try:
        lang4 = soup.html['lang']
        # print("lang : --->",lang4)
        langs.append(lang4)
    except:
        pass
    try:
        keyword = soup.findAll(attrs={"name": re.compile(r"keyword", re.I)})
        keyword = keyword[0]['content']if keyword else ""
    except:
        pass
    titles = set(titles) - {None}
    descps = set(descps) - {None}
    langs = set(langs) - {None}

    titles = list(i.replace(',',' ').replace("\n"," ") for i in titles)
    descps = list(i.replace(',',' ').replace("\n"," ") for i in descps)
    langs = list(i.replace(',',' ').replace("\n"," ") for i in langs)

    keyword = keyword.replace(',',' ').replace("\n"," ")
    #
    titlesString = ''
    for j in titles:
        titlesString = titlesString + ' ' + j
    titlesString = titlesString.strip()

    descString = ''
    for j in descps:
        descString = descString + ' ' + j
    descString = descString.strip()

    langString = ''
    for j in langs:
        langString = langString + ' ' + j
    langString = langString.strip()
    # print("titlesString :",titlesString)
    # print("descString :",descString)
    # print("langString :",langString)
    # print("keyword :",keyword)

    return titlesString,descString,langString,keyword
    # return


if(__name__ == '__main__'):
    if(len(sys.argv) == 2):
        path = sys.argv[1]
    elif(len(sys.argv) > 2):
        print('Too many parameters')
        exit(0)
    else:
        path = './top-1m-websites.csv'
    main()
