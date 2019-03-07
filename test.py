import socket
import pandas as pd
import numpy as np
import requests
import traceback
from os import path,mkdir
from bs4 import BeautifulSoup
import sys
import re
def openFiles():
    from os import path
    if(path.exists('./data.csv')):
        finalFile = open('data.csv','a')
    else:
        finalFile = open('data.csv','a')
        finalFile.write("slno,hostname,alias,ipaddress,titles,description,language,keyword\n")

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
    return finalFile,aliasFile,fetchFile

def readData(path):
    try:
        return pd.read_csv('./top-1m-websites.csv',)
    except:
        print("Error in reading input file")

def main():
    finalFile,aliasFile,fetchFile = openFiles()
    # return
    start = 2
    end = 3
    csvData = readData(path)
    topTen = csvData[start:end]

    def handleAliasError(err):
        aliasFile.write(slno+','+url+'\n')
        traceback.print_exc()

    def handleFetchError(err):
        fetchFile.write(slno+','+url+'\n')
        traceback.print_exc()

    for i in range(0,end - start):
        url = 'www.'+str(topTen['websiteName'][start + i])
        slno = str(topTen['slno'][start + i])
        try:
            hostData = socket.gethostbyname_ex(url)
            hostName = hostData[0]
            aliases = hostData[1]
            ipAddress= hostData[2]
            # Todo handle unicode in hostname,aliases
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
            handleAliasError(e)
            continue
        try:
            url = 'https://' + url
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            websiteData = soup.prettify()
            # titlesString,descString,langString,keyword = getDetails(soup)
            getDetails(soup)


            # finalString = ''+slno+','+url+','+aliasString+','+ipString+','+titlesString+','+descString+','+langString+','+keyword+'\n'
            finalString = ''+slno+','+url+','+aliasString+','+ipString+'\n'
            finalFile.write(finalString)
            print(slno)

            with open('./WebPages/'+slno+'.html','w') as webPageFile:
                webPageFile.write(websiteData)
            # with open(slno+'_'+hostname+'.html')
            # break
        except Exception as e:
            handleFetchError(e)

def getDetails(soup):
    titles = []
    descps = []
    langs = []
    title1=str(soup.title)
    title1=title1.replace("<title>","")
    titles.append(title1.replace("</title>",""))

    title2 = soup.find("meta",  property="og:title")
    titles.append(title2["content"] if title2 else None)

    title3 = soup.find("meta",  property="twitter:title")
    titles.append(title3["content"] if title3 else None)

    title4 = soup.findAll(attrs={"name": re.compile(r"title", re.I)})
    titles.append(title4[0]['content'] if title4 else None)

    desc1 = soup.find("meta",  property="og:description")
    descps.append(desc1["content"] if desc1 else None)

    desc2 = soup.find("meta",  property="twitter:description")
    descps.append(desc1["content"] if desc2 else None)

    desc3 = soup.findAll(attrs={"name": re.compile(r"description", re.I)})
    descps.append(desc3[0]['content']if desc3 else None)

    lang1 = soup.findAll(attrs={"http-equiv": re.compile(r"lang", re.I)})
    langs.append(lang1[0]['content']if lang1 else None)

    lang2 = soup.findAll(attrs={"name": re.compile(r"lang", re.I)})
    langs.append(lang2[0]['content']if lang2 else None)

    lang3 = soup.findAll(attrs={"lang": re.compile(r"lang", re.I)})
    langs.append(lang3[0]['content']if lang3 else None)

    keyword = soup.findAll(attrs={"name": re.compile(r"keyword", re.I)})
    keyword = keyword[0]['content']if keyword else ""

    titles = set(titles) - {None}
    descps = set(descps) - {None}
    langs = set(langs) - {None}

    # titles = list(i.replace(',',' ') for i in titles)
    # descps = list(i.replace(',',' ') for i in descps)
    # langs = list(i.replace(',',' ') for i in langs)
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
    print(titles)
    print(descps)
    print(langs)

    # return titlesString,descString,langString,keyword
    return


if(__name__ == '__main__'):
    if(len(sys.argv) == 2):
        path = sys.argv[1]
    elif(len(sys.argv) > 2):
        print('Too many parameters')
        exit(0)
    else:
        path = './top-1m-websites.csv'
    main()
