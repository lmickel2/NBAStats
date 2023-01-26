import requests
from bs4 import BeautifulSoup

year=input("Which NBA season are you interested in?: ")
player=input("For which player do you want to get stats?: ").lower()

# Takes players name splits into parts that go into the url
def getUrlComponents(player):
    firstLastName = player.split(" ")
    components = ["", ""]
    components[0] = firstLastName[1][0]
    components[1] = firstLastName[1][:5] + firstLastName[0][:2]
    return components

#Iterates through urls using components of users name until right url is found
def getUrl(year, player):
    components = getUrlComponents(player)
    playerName = player.split(" ")
    url = ""
    try:
        vals = range(4)
        for i in vals:
            num = "0" + str(i)
            testUrl = "https://www.basketball-reference.com/players/{}/{}{}/gamelog/{}".format(components[0], components[1], num, year)
            response = requests.get(testUrl)
            soup = BeautifulSoup(response.text, 'html.parser')
            header = soup.h1.text
            headerText = header[1:-1]
            headerComponents = headerText.split(" ")
            firstName = headerComponents[0].lower()
            lastName = headerComponents[1].lower()
            if(firstName == playerName[0] and lastName == playerName[1]):
                url = testUrl
                break
    except:
        print("Could not find player")
        exit()
    return url

url = getUrl(year, player)
print(url)

