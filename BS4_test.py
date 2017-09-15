import certifi
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)
for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])

###################################################################
import certifi
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html,"lxml")
for link in bsObj.find("div",{"id":"bodyContent"}).findAll("a", href = re.compile(
        "^(/wiki/)((?!:)*$)")):
    if 'href' in link.attrs:
        print(link.attrs['href'])


###################################################################

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("https://en.wikipedia.org"+articleUrl)
    bsObj1 = BeautifulSoup(html, "lxml")
    return bsObj1.find("div",{"id":"bodyContent"}).findAll("a",
                    href = re.compile("^(/wiki)((?!:).)*$"))
links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)

###################################################################

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("https://en.wikipedia.org" + pageUrl)
    bsObj2 = BeautifulSoup(html, "lxml")
    for link in bsObj2.findALL("a", href = re.compile("^(/wiki)")):
        if 'href' in links.attrs:
            if links.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")

###################################################################

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("https://en.wikipedia.org" + pageUrl)
    bsObj3 = BeautifulSoup(html, "lxml")
    try:
        print(bsObj3.h1.get_text())
        print(bsObj3.find(id = "mw-content-text").findAll("p")[0])
        print(bsObj3.find(id = "ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! That's OK!")

    for link in bsObj3.findAll("a", href = re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in page:
                newPage = link.attrs['href']
                print("------------------\n" + newPage)
                page.add(newPage)
                getLinks(newPage)


###################################################################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def getInternalLinks(bsObj4, includeUrl):
    internalLinks = []
    for link in bsObj4.findAll("a", href = re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs[href] is not None:
            if links.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks
def getExternalLinks(bsObj, excluderUrl):
    externalLinks = []
    for link in bsObj.findAll("a",
                              href = re.compile("^(http|www)((?!"+excluderUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks: externalLinks.append(link.attrs['href'])
        return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0,
        len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink("http://oreilly.com")
    print("Random external link is: "+externalLink)
    followExternalOnly(externalLink)
followExternalOnly("http://oreilly.com")


#####################################################################################


