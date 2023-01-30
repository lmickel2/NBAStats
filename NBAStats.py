import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import sys
#sys.tracebacklimit = 0

while True:
    year=input("Which NBA season are you interested in?: ")
    if (year.isdigit() == True and (len(year) == 4)):
        currentyear = int(year)
        if ((currentyear <= datetime.now().year and currentyear >= 1946)):
            for i in range(4):
                player=input("For which player do you want to get stats?: ").lower()
                if (all(x.isalpha() or x.isspace() for x in player)) and " " in player:
                    break
                elif (all(x.isalpha() for x in player)):
                    print("Are you typing only a first or last name? Or did you forget to add a space between the two?")
                    NameRes = input("Type 'First' for first name. Type 'Last' for last name, or 'Try again' if you forgot a space or know the part of the name you're missing.").lower()
                    print(NameRes)
                    if NameRes == "first":
                        print(player)
                        url = "https://www.statmuse.com/nba/ask/{}".format(player)
                        print(url)
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        check = soup.findAll("td", attrs={"class":"text-left px-2 py-1 sticky left-0 bg-white"})
                        print(check)
                        for names in check:
                            print("Did you mean?", names.find("a".text))
                if i == 3:
                    print("Either the player you are looking for does not exist in this database, or you are misspelling their name.")
                    exit()
        else:
            print("The year you input was invalid. Try again.")
            continue
    else:
        print("The year you input was invalid. Try again.")
        continue
    break

# Takes players name splits into parts that go into the url
def getUrlComponents(player):
        firstLastName = player.split(" ")
        components = ["", ""]
        components[0] = firstLastName[1][0]
        components[1] = firstLastName[1][:5] + firstLastName[0][:2]
        return components

#Iterates through urls using components of users name until right url is found
#Returns website soup
def getUrl(year, player):
    components = getUrlComponents(player)
    playerName = player.split(" ")
    try:
        vals = range(4)
        for i in vals:
            num = "0" + str(i)
            url = "https://www.basketball-reference.com/players/{}/{}{}/gamelog/{}".format(components[0], components[1], num, year)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            header = soup.h1.text
            headerText = header[1:-1]
            headerComponents = headerText.split(" ")
            firstName = headerComponents[0].lower()
            lastName = headerComponents[1].lower()
            if(firstName == playerName[0] and lastName == playerName[1]):
                print("All stats pulled from: ", url)
                return soup
    except:
        print("Could not find player")
        exit()

soup = getUrl(year, player)
#table = soup.findAll("table")
#print(table)
