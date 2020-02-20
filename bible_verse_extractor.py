#! /usr/bin/env python3

import requests
import bs4 as bs
import re

codePattern = re.compile('(?<=\().{3}(?:_.{2,3})?(?=\))')

#language = input("Choose a language: ")
#link = 'http://www.bible.com/en/languages/{}'.format(language)

def checkDownload(downloadedPage):
    try:
        return downloadedPage.raise_for_status()
    except:
        print("Download failed.")

language = 'tgl'
mainPage = 'http://www.bible.com/languages'

def getPage(link):
    page = requests.get(mainPage)
    checkDownload(page)
    soupPage = bs.BeautifulSoup(page.text, features='lxml')
    return soupPage

def getLanguageList(soupObject):
    languageLinks = soupObject.select('td > a')
    languageList = dict()
    for languageLink in languageLinks:
        try:
            languageCode = re.search(codePattern, languageLink.get('title')).group()
            languageList[languageCode] = languageLink.getText().strip()
        except:
            continue
    return languageList, languageLinks

def getLanguage(language, languageList, languageLinks):
    for code, name in languageList.items():
        if language in code or language in name:
            for languageLink in languageLinks:
                try:
                    if code in languageLink.get('title') and name in languageLink.getText():
                        return languageLink.get('href')
                except:
                    continue

def getTranslationList(soup):
    translationList = list()
    for item in soup.find_all('a'):
        print(item.get('href'))
        if 'versions' in item:
            print(item)
            translationList.append(item.getText())
    return translationList 

mainPageSoup = getPage(mainPage)
languageList, languageLinks = getLanguageList(mainPageSoup)
link = getLanguage(language, languageList, languageLinks)
translationListSoup = getPage(mainPage + link[10:])
translationList = getTranslationList(translationListSoup)
print(translationList)
#link = 'http://www.bible.com/en/bible/177/MAT.10.TLAB'
#biblePage = requests.get(link)
#checkDownload(biblePage)

#soupBible = bs.BeautifulSoup(biblePage.text, features='lxml')
#spans = soupBible.select('span')
#for span in spans:
#    if ' '.join(span.get('class')) == 'verse v29':
#        print(span)

#print(len(verse))
#TODO: Access a particular bible translation

#TODO: Access a chapter

#TODO: Copy a verse

#TODO: Save to a file
#with open('bible_{}.csv', 'wb') as saveFile:
#    for chunk in biblePage.iter_content(100000):
#       saveFile.write(chunk)

