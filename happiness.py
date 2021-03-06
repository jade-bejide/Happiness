'''Profession options:
    0. Unemployed
    1. Low income
    2. Middle income
    3. High income
    4. Aristocrat
'''

import random
import json

#To add:
#4 can only have 4 and 3 friends
#3 can have 2, 3, and 4 friends
#2 can have 0, 1, 2 and 3 friends
#1 can have 0, 1 and 2 frinds
#0 can have 0, 1 and 2 friends

class Community(object):
    def __init__(self, name):
        self._name = name
        self._inhabitants = []
        #links acquaintance pairs as dictionaries

    def addToCommunity(self, inhabitant):
        self._inhabitants.append(inhabitant)

    def automateAcquaintances(self):
        #people have from five to about half the number of inhabitants in the community as friends
        
        for i in range(0, len(self._inhabitants)):
            numOfFriends = random.randint(5,len(self._inhabitants)//2)
            for j in range(0, numOfFriends-1):
                #creates a list of potential friends
                availableFriends = []
                for k in range(0, len(self._inhabitants)):
                    if k != i:
                        availableFriends.append(k)

                #finds position of friend
                pos = random.choice(availableFriends)
                status = self._inhabitants[i].getProfession()
                if status == 0:
                    if self._inhabitants[pos].getProfession() == 0 or self._inhabitants[pos].getProfession() == 1 or self._inhabitants[pos].getProfession() == 2:
                            self._inhabitants[i].makeAcquaintances(self._inhabitants[pos])
                            self._inhabitants[pos].makeAcquaintances(self._inhabitants[i])
                elif status == 1:
                    if self._inhabitants[pos].getProfession() == 0 or self._inhabitants[pos].getProfession() == 1 or self._inhabitants[pos].getProfession() == 2:
                        self._inhabitants[i].makeAcquaintances(self._inhabitants[pos])
                        self._inhabitants[pos].makeAcquaintances(self._inhabitants[i])
                elif status == 2:
                    if self._inhabitants[pos].getProfession() == 0 or self._inhabitants[pos].getProfession() == 1 or self._inhabitants[pos].getProfession() == 2 or self._inhabitants[pos].getProfession() == 3:
                        self._inhabitants[i].makeAcquaintances(self._inhabitants[pos])
                        self._inhabitants[pos].makeAcquaintances(self._inhabitants[i])
                    
                elif status == 3:
                    if self._inhabitants[pos].getProfession() == 2 or self._inhabitants[pos].getProfession() == 3 or self._inhabitants[pos].getProfession() == 4:
                        self._inhabitants[i].makeAcquaintances(self._inhabitants[pos])
                        self._inhabitants[pos].makeAcquaintances(self._inhabitants[i])
                elif status == 4:
                    if self._inhabitants[pos].getProfession() == 3 or self._inhabitants[pos].getProfession() == 4:
                        self._inhabitants[i].makeAcquaintances(self._inhabitants[pos])
                        self._inhabitants[pos].makeAcquaintances(self._inhabitants[i])
                    



    def calculateHappiness(self):
        for i in range(0, len(self._inhabitants)-1):
            self._inhabitants[i].setHappiness()

    def getCommunityHappiness(self):
        happyList = []

        random.shuffle(self._inhabitants)
        for i in range(0, len(self._inhabitants)-1):
            #reformat acquaintance list to show names
            friends = []
            for k in range(0, len(self._inhabitants[i].getAcquaintances())-1):
                friends.append(self._inhabitants[i].getAcquaintances()[k].getName())
            template = {"name": " ", "profession": None, "Friends": None, "Number of Friends": None, "happiness": 0}
            template["name"] = self._inhabitants[i].getName()
            template["profession"] = self._inhabitants[i].getProfession()
            template["Friends"] = friends
            template["Number of Friends"] = len(self._inhabitants[i].getAcquaintances())-1
            template["happiness"] = round(self._inhabitants[i].getHappiness(),2)

            happyList.append(template)

        return happyList
        
class Person(object):
    def __init__(self, name, profession):
        #string
        self._name = name
        #integer
        self._profession = profession
        #integer
        self._happiness = 20
        #list
        self._acquaintances = []

    def getName(self):
        return self._name

##    def makeAcquaintancesWith(self, friend):
##        self._acquaintances.append(friend)
        
    def makeAcquaintances(self, friend):
        #connects two people in a community as friends
        if friend not in self._acquaintances:
            self._acquaintances.append(friend)

    def getAcquaintances(self):
        return self._acquaintances

    def getProfession(self):
        return self._profession

    def downgradeProfession(self):
        if self._profession > 0:
            self._profession -= 1

    def upgradeProfession(self):
        '''a person cannot upgrade to aristocrat - this is
        because this is unrealistic in real application terms, allocation
        of aristocrats will be limited and at random'''
        if self._profession < 3:
            self._profession += 1

    def setHappiness(self):
        '''Happiness is updated on two main factors: income and acquintances'''

        #modelling the easterlin paradox
        if len(self._acquaintances) > 0:
            avgProfession = 0
            for pal in range(0, len(self._acquaintances)):
                avgProfession += self._acquaintances[pal].getProfession()

            if avgProfession > 0:
                avgProfession = avgProfession / len(self._acquaintances)
                avgProfession = round(avgProfession, 2)

                if avgProfession > self._profession:
                    difference = avgProfession - self._profession
                    self._happiness = self._happiness * (1 - (difference/100))
                elif avgProfession < self._profession:
                    difference = self._profession - avgProfession
                    self._happiness = self._happiness * (1+ (difference/100))
                
            #starting from the start of the list - assuming that oldest friends are most influential on happiness


            #splitting the list of acquaintances into a distribution, modelling on the assumption that a person typically has at least 5 friends (to change)
            distribution = len(self._acquaintances) // 5
            n = 1

            random.shuffle(self._acquaintances)
            for i in range(0, len(self._acquaintances)):
                #influence on happiness decreases as you get to the most recent acquaintances, stretched across the distribution contanst
                increaseFactor = (0.5)**n
                self._happiness += self._acquaintances[i].getHappiness() * (increaseFactor)
                if i % 5 == 0 and n < (distribution +1):
                    n += 1

        else:
            self._happiness = self._happiness * 0.5

    def getHappiness(self):
        return self._happiness

#Instantiate members of a community
andy = Person("andy", random.randint(0,4))
beth = Person("beth", random.randint(0,4))
celia = Person("celia", random.randint(0,4))
darren = Person("darren", random.randint(0,4))
emily = Person("emily", random.randint(0,4))
faith = Person("faith", random.randint(0,4))
georgia = Person("georgia", random.randint(0,4))
harry = Person("harry", random.randint(0,4))
isla = Person("isla", random.randint(0,4))
jade = Person("jade", random.randint(0,4))
kyan = Person("kyan", random.randint(0,4))
layla = Person("layla", random.randint(0,4))
mandy = Person("mandy", random.randint(0,4))
nnandi = Person("nnandi", random.randint(0,4))
oliver = Person("oliver", random.randint(0,4))
penelope = Person("penelope", random.randint(0,4))
quiana = Person("quiana", random.randint(0,4))
rowan = Person("rowan", random.randint(0,4))
sissy = Person("sissy", random.randint(0,4))
tony = Person("tony", random.randint(0,4))
ursala = Person("ursala", random.randint(0,4))
vivian = Person("vivian", random.randint(0,4))
warren = Person("warren", random.randint(0,4))
xander = Person("xander", random.randint(0,4))
yara = Person("yara", random.randint(0,4))
zach = Person("zach", random.randint(0,4))

communityX = Community("Community X")

#add people to community at random
people = [andy, beth, celia, darren, emily, faith, georgia, harry,
          isla, jade, kyan, layla, mandy, nnandi, oliver, quiana, rowan,
          sissy, tony, ursala, vivian, warren, xander, yara, zach]

numOfPeople = len(people)

for i in range(0, numOfPeople-1):
    person = random.choice(people)
    communityX.addToCommunity(person)
    people.remove(person)

communityX.automateAcquaintances()
communityX.calculateHappiness()
happyList = communityX.getCommunityHappiness()

with open("happiness.json", "w") as file:
    for line in happyList:
        json.dump(line, file)
        file.write("\n")
        file.write("\n")
##for row in happyList:
##    print(row)
##    print("\n")

        


