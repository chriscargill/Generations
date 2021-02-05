"""
A population simulator that starts with a given population size and calculates the population growth each year. Press Q to stop the simulation or R to restart it. Then check the file created (./history) to see how many years past and the births and deaths of all the people.
"""

## IMPORTS
import pygame
from pygame.locals import *
import time
import subprocess, signal, os
from random import *
from datetime import datetime
from colors import *
import math
pygame.init()


## COLORS
# Colors indicate the lineage
blue = BLUE
deathblue = LIGHTBLUE
teal = TEAL
yellow = YELLOW
orange = ORANGE
green = GREEN

black = BLACK
deathvermillion = LIGHTRED
vermillion = RED
lemon = TAN
deathlemon = LIGHTTAN

white = WHITE
grey = GRAY
darkblue = DARKBLUE
deepblue = (11,40,82)
darkgreen = DARKGREEN
myFavFont = 'Arial'

MATING_RANGE = 40
HOME_RANGE = 500

## SIZES
# Sizes indicate the generation
FifthGen = 0
FourthGen = 10
ThirdGen = 13
SecondGen = 16
FirstGen = 20

## SCREEN
currentMonitor = pygame.display.Info()
game_display_width = int(currentMonitor.current_w)
game_display_height = int(currentMonitor.current_h)
gamedisplayBackground = black
gameDisplay = pygame.display.set_mode((game_display_width, game_display_height))
pygame.display.set_caption('Generations')
wcenter = game_display_width/2
hcenter = game_display_height/2
center = (wcenter,hcenter)
gameDisplay.fill(gamedisplayBackground)

#create a clock for the game to help with organizing frames per second
game_clock = pygame.time.Clock()


## GLOBAL VARIABLES
sectionW = 0
sectionH = 0

CID = 1
AdamGenome = []
EveGenome = []
AdamChromosomes = [11,22,21,12]
EveChromosomes = [33,44,34,43]
AdamLineOne = []
AdamLineTwo = []
EveLineOne = []
EveLineTwo = []
ChildDNA1 = []
ChildDNA2 = []
ChildDNATotal = []
childDictionary = {}
girlNames = []
boyNames = []
matedList = []
diedList = []
marriedList = []
deadListWrite = []
years = 0
bornList = []
removeSpouse = []
removePerson = []
childHoldingDictionary = {}
trackErrors = []
mygirls = open('girlnames', 'r')
for line in mygirls:
    names = line.split('*')
    for name in names:
        girlNames.append(name)
myboys = open('boynames', 'r')
for line in myboys:
    names = line.split('*')
    for name in names:
        boyNames.append(name)


## CLASSES

class Child:
    def __init__(self, CID, dna, name, age, gender, parent1, parent2):
        self.id = CID
        self.dna = dna
        self.name = name
        self.age = age
        self.gender = gender
        self.maxage = randint(130, 950)
        self.dad = parent1
        self.mom = parent2
        self.x = randint(0, game_display_width-10)
        self.y = randint(0, game_display_height-10)
        self.mated = False
        self.spouse = None
        self.spouse_id = None
        self.home_x = None
        self.home_y = None
        idIncrement()
        # print(f"{self.name}({self.gender}) has been born.")

    def __repr__(self):
        return f"Object {self.name}({self.gender}) is {self.age} years old."

    def __str__(self):
        return f"{self.name}({self.gender}):"

## FUNCTIONS
def inRange(obj1, obj2, max_distance):
    """
    (Child, Child, int) -> Boolean
    (Child, None, int) -> Boolean
    (tuple, tuple, int) -> Boolean
    """
    if type(obj1) == tuple and type(obj2) == tuple: # If instead of objects tuples are sent
        x, y = obj1
        x2, y2 = obj2
        distance_x = abs(x - x2)
        if distance_x > max_distance:
            return False
        distance_y = abs(y - y2)
        if distance_y > max_distance:
            return False
        distance_squared = (distance_x * distance_x) + (distance_y * distance_y) # Pythagorus theorem
        distance = math.sqrt(distance_squared)
        if distance <= max_distance:
            return True
        else:
            return False
    elif obj2 != None: # If both are objects
        distance_x = abs(obj1.x - obj2.x)
        if distance_x > max_distance:
            return False
        distance_y = abs(obj1.y - obj2.y)
        if distance_y > max_distance:
            return False
        distance_squared = (distance_x * distance_x) + (distance_y * distance_y) # Pythagorus theorem
        distance = math.sqrt(distance_squared)
        if distance <= max_distance:
            return True
        else:
            return False
    else: # If object2 is None, check range to object1's home
        try:
            distance_x = abs(obj1.x - obj1.home_x)
            if distance_x > max_distance:
                return False
            distance_y = abs(obj1.y - obj1.home_y)
            if distance_y > max_distance:
                return False
            distance_squared = (distance_x * distance_x) + (distance_y * distance_y) # Pythagorus theorem
            distance = math.sqrt(distance_squared)
            if distance <= max_distance:
                return True
            else:
                return False
        except Exception as e:
            trackErrors.append(e)
            return False


def writeToFile(theList, fileName, style):
    myfile = open(fileName, style)
    myfile.write(f"{years} years:\n")
    myfile.write(f"{str(CID)} \n")
    myfile.write("\n")
    for item in theList:
        myfile.write(f"{item}\n")
    myfile.write("\n\n\n")
    myfile.close()

def writeToFiles(style):
    writeToFile(bornList, "Births.txt", style)
    writeToFile(deadListWrite, "Deaths.txt", style)
    writeToFile(marriedList, "Marriages.txt", style)
    writeToFile(matedList, "Mated.txt", style)

def setHome(obj):
    obj.home_x = obj.x
    obj.home_y = obj.y


def freeToMateNoSpouse(child, iteratableDictionary):
    for person in iteratableDictionary.values():
        if person.age > 12:
            if person.gender != child.gender: # if the person is a different gender
                if not person.spouse_id and not child.spouse_id: # If the person has no spouse and the child has no spouse
                    if inRange(child, person, MATING_RANGE): # if they are within range:
                        mate(child,person)
                        marriedList.append(f"{child.name}({child.gender}: {child.id}) married {person.name}({person.gender}: {person.id})")
                        setHome(child)
                        setHome(person)
                        break

                    else: # if they are not in range
                        pass
                else: # if the child has a spouse or the person has a spouse
                    pass
            else: # same gender, can't mate
                pass
        else:
            pass


def freeToMateWithSpouse(child):
    if inRange(child, child.spouse, MATING_RANGE):
        mate(child,child.spouse)


def checkAround():
    iteratableDictionary = {}
    for child in childDictionary.values():
        # Add child to other dictionary
        if child.age > 12:
            if not child.mated and not child.spouse: # If the child is free to mate and has no spouse
                iteratableDictionary[child.id] = child
                freeToMateNoSpouse(child,iteratableDictionary)
            elif not child.mated and child.spouse: # If the child is free to mate but has a spouse
                freeToMateWithSpouse(child)
            else: # the child is not free to mate
                pass
        else:
            pass
            
def idIncrement():
    global CID
    CID += 1

def quitGame(event):
    if event.type == pygame.QUIT:
        window_closed = True

def CreateAdamEve():
    global AdamGenome
    global EveGenome
    for item in range(10):
        index = randint(0, 3)
        AdamGenome.append(AdamChromosomes[index])
    for item in range(10):
        index = randint(0, 3)
        EveGenome.append(EveChromosomes[index])

def StripParentDNA():
    global AdamGenome
    global AdamLineOne
    global AdamLineTwo
    global EveGenome
    global EveLineOne
    global EveLineTwo
    for item in AdamGenome:
        strDigit = str(item)
        firstDigit = strDigit[0]
        secondDigit = strDigit[1]
        AdamLineOne.append(firstDigit)
        AdamLineTwo.append(secondDigit)
    for item in EveGenome:
        strDigit = str(item)
        firstDigit = strDigit[0]
        secondDigit = strDigit[1]
        EveLineOne.append(firstDigit)
        EveLineTwo.append(secondDigit)

def CreateChildDNAFromAdamEve():
    global ChildDNA1
    global ChildDNA2
    global ChildDNATotal
    # Select whcih line from adam to use
    index = randint(0,1)
    if (index == 0):
        ChildDNA1 = AdamLineOne
    else:
        ChildDNA1 = AdamLineTwo
    # Select which line from eve to use
    index = randint(0,1)
    if (index == 0):
        ChildDNA2 = EveLineOne
    else:
        ChildDNA2 = EveLineTwo
    # Combine the two selected lines together
    for item in range(10):
        ChildDNATotal.append(ChildDNA1[item] + ChildDNA2[item])

def CreateKid(CID, dna,name, gender, dad, mom, dad_id, mom_id):
    global childDictionary
    global bornList
    newChild = Child(CID, dna, name, 0, gender, dad, mom)
    childHoldingDictionary[CID] = newChild # Add child to holding dictionary
    bornList.append(f"{name}({gender}: {CID}) was born from {dad}({dad_id}) and {mom}({mom_id}).")


def changeAge():
    global childDictionary
    global diedList
    for person_id, person in childDictionary.items():
        person.age += 1
        if person.age > person.maxage:
            if person.gender == "M":
                deadListWrite.append(f"{person}({person.id}) Born of {person.dad} and {person.mom} lived to be {person.age} years old and then he died.")
                diedList.append(person)
            else:
                deadListWrite.append(f"{person}({person.id}) Born of {person.dad} and {person.mom} lived to be {person.age} years old and then she died.")
                diedList.append(person)
            removeSpouse.append(person)
            removePerson.append(person)


def removeDead():
    if len(removePerson) > 0:
        for item in removeSpouse:
            if item != None:
                try:
                    childDictionary[item.spouse_id].spouse_id = None # Widow the spouse
                    childDictionary[item.spouse_id].home_x = None
                    childDictionary[item.spouse_id].home_y = None
                except Exception as e:
                    trackErrors.append(f"RemoveDead() {e}")
        removeSpouse.clear()
        for item in removePerson:
            if item != None:
                try:
                    print(f"KILLING {item}")
                    del childDictionary[item.id] # Mark this person as no longer living
                except Exception as e:
                    trackErrors.append(f"removeDead() {e}")
        removePerson.clear()


def drawPeople():
    gameDisplay.fill(gamedisplayBackground)
    if CID < 10000:
        for person in childDictionary.values():
            try:
                if person.gender == 'M':
                    pygame.draw.circle(gameDisplay, blue, (person.x, person.y), 5)
                else:
                    pygame.draw.circle(gameDisplay, lemon, (person.x, person.y), 5)
            except Exception as e:
                trackErrors.append(f"DrawPeople(): {e}")

    if len(diedList) < 1000:
        for person in diedList:
            try:
                if person.gender == 'M':
                    pygame.draw.circle(gameDisplay, deathblue, (person.x, person.y), 8)
                else:
                    pygame.draw.circle(gameDisplay, deathlemon, (person.x, person.y), 8)
            except Exception as e:
                trackErrors.append(f"drawpeople(): {e}")
def movePeople():
    for person in childDictionary.values():
        try:
            if person.spouse: # If the person has a spouse
                if not inRange(person,None,HOME_RANGE): # If the person is not in range of their home send them home:
                    person.x = person.home_x
                    person.y = person.home_y 
            person.x = person.x + randint(-40, 40)
            while person.x < 20:
                person.x += 10
            while person.x > game_display_width-20:
                person.x -= 10 
            person.y = person.y + randint(-40, 40)
            while person.y < 20:
                person.y += 10
            while person.y > game_display_height-80:
                person.y -= 10 
        except Exception as e:
            trackErrors.append(f"movePeople(): {e}:{person.x},{person.y}/{person.home_x},{person.home_y}")


def createNewKid(person1, person2):
    gender = randint(0,1)
    if gender == 0:
        childGender = "M"
        CreateKid(CID, ChildDNATotal, boyNames[randint(0,len(boyNames)-1)], "M", person1.name, person2.name, person1.id, person2.id)

    else:
        childGender = "F"
        CreateKid(CID, ChildDNATotal, girlNames[randint(0,len(girlNames)-1)], "F", person1.name, person2.name, person1.id, person2.id)


def createFirstKids():
    for i in range(0,3):
        CreateKid(CID, ChildDNATotal, boyNames[randint(0,len(boyNames)-1)], "M", "Adam", "Eve", -1, 0)
        CreateChildDNAFromAdamEve()
    for i in range(0,3):
        CreateKid(CID, ChildDNATotal, girlNames[randint(0,len(girlNames)-1)], "F", "Adam", "Eve", -1, 0)
        CreateChildDNAFromAdamEve()

def mate(person1, person2):
    global matedList
    if person1.mated == False and person2.mated == False:
        matedList.append(f"{person1} ({person1.id}) and {person2} ({person2.id}) have mated!")
        # We only stop the person from mating again until the next frame if they are a female
        if person1.gender == "F":
            person1.mated = True
        if person2.gender == "F":
            person2.mated = True

        createNewKid(person1, person2)

        person1.spouse = person2
        person1.spouse_id = person2.id
                            
        person2.spouse = person1
        person2.spouse_id = person1.id
        #Split DNA here and create a new child


def addNewKidsToDictionary():
    for key,value in childHoldingDictionary.items():
        childDictionary[key] = value
    childHoldingDictionary.clear()


def setup():
    CreateAdamEve()
    StripParentDNA()
    CreateChildDNAFromAdamEve()
    createFirstKids()

def ableToMate():
    for child in childDictionary.values():
        child.mated = False

def reset():
    global CID, AdamGenome, EveGenome, AdamChromosomes, EveChromosomes, AdamLineOne, AdamLineTwo, EveLineOne, EveLineTwo, ChildDNA1, ChildDNA2, ChildDNATotal, childDictionary, girlNames, boyNames, matedList, diedList, deadListWrite, years, bornList
    CID = 1
    AdamGenome = []
    EveGenome = []
    AdamChromosomes = [11,22,21,12]
    EveChromosomes = [33,44,34,43]
    AdamLineOne = []
    AdamLineTwo = []
    EveLineOne = []
    EveLineTwo = []
    ChildDNA1 = []
    ChildDNA2 = []
    ChildDNATotal = []
    childDictionary = {}
    girlNames = []
    boyNames = []
    matedList = []
    diedList = []
    marriedList = []
    deadListWrite = []
    years = 0
    bornList = []
    removeSpouse = []
    removePerson = []
    mygirls = open('girlnames', 'r')
    for line in mygirls:
        names = line.split('*')
        for name in names:
            girlNames.append(name)
    myboys = open('boynames', 'r')
    for line in myboys:
        names = line.split('*')
        for name in names:
            boyNames.append(name)
    print("\n\n")

    setup()

## GAME LOOP

setup()


window_closed = False
while not window_closed:

    for event in pygame.event.get():
        # everyEvent(event)
        if event.type == pygame.KEYDOWN:
            # print("Key pressed")
            for keypressed in event.unicode:
                # print(keypressed)
                #Quit the game
                if keypressed == 'q':
                    writeToFiles("w")
                    for eachError in trackErrors:
                        print(eachError)
                    pygame.quit()
                    quit()
                if keypressed == 'r':
                    writeToFiles("a")
                    reset()
    
    pygame.display.flip()
    pygame.event.pump()
    #Handles frames per second: (60 seconds per second)
    game_clock.tick(30)
    years +=1
    changeAge()
    removeDead()
    drawPeople()
    movePeople()
    checkAround()
    addNewKidsToDictionary()
    ableToMate()
    if years % 50 == 0:
        print(years, CID)
#Quit pygame
pygame.quit()
#Quit application
quit()