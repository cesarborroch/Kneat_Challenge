# Library used to return the content of a URL
from urllib.request import Request, urlopen
# Library to decode text to JSON
import json

class SW_stops_amount:

    def __init__(self):
        pass

    # Decodes the consumables
    def calc(self, strConsumables):
        intHOURS_IN_YEAR = 8760
        intHOURS_IN_MONTH = 730
        intHOURS_IN_WEEK = 168
        intHOURS_IN_DAY = 24    
        
        # Gets the number part of the string
        strValue = ''
        for s in strConsumables.split():
            if s.isdigit():
                strValue += s         
        intNumber = int(strValue)

        # Interprets the text part in consumables
        if 'day' in strConsumables:
            return intNumber * intHOURS_IN_DAY
        if 'week' in strConsumables:
            return intNumber * intHOURS_IN_WEEK
        if 'month' in strConsumables:
            return intNumber * intHOURS_IN_MONTH
        if 'year' in strConsumables:
            return intNumber * intHOURS_IN_YEAR

    def get_amount(self, intDistance, strConsumables, strMGLT):
        return int(intDistance / (self.calc(strConsumables) * int(strMGLT)))

    # Prints the amount of stops given the ship and distance
    def analyze_ship(self, ship, intDistance):
        # Calculates the amount of stops
        strName = ship['name']
        strConsumables = ship['consumables']
        strMGLT = ship['MGLT']

        # Can't calculate when certain values are missing
        if strConsumables != 'unknown' and strMGLT != 'unknown':
            intAmountOfStops = self.get_amount(intDistance, strConsumables, strMGLT)
            print('Ship: "{}", Amount of stops: {}'.format(strName, intAmountOfStops))
        else:
            print('Ship: "{}", Consumables and/or MGLT are unknown.'.format(strName))

    def run(self):
        # Header
        print('Amount of Stops Calculator for SW Ships')
        print()

        # Asks the user for a value
        bAskingForInput = True
        while bAskingForInput:
            try:
                print('How far are you heading? Insert a numerical value for a distance in MGLT.')
                strInput = input()
                intDistance = int(strInput)
                bAskingForInput = False
            except:
                print('The inserted value "{}" is invalid as a number. Try again.'.format(strInput))

        print()
        strURL_SWAPI_STARSHIPS = 'https://swapi.co/api/starships/'
        print('Downloading data from {}...'.format(strURL_SWAPI_STARSHIPS))
        print()

        # Controls how many pages should be read
        bThereIsMoreData = True;
        intAmountOfShips = 0
        while bThereIsMoreData:  
            # Gets the starships and their data
            req = Request(strURL_SWAPI_STARSHIPS, headers={'User-Agent': 'Mozilla/5.0'})
            content = urlopen(req).read()
            data = json.loads(content.decode())

            # Does the calc for each starship
            for ship in data['results']:
                intAmountOfShips += 1
                self.analyze_ship(ship, intDistance)

            strURL_SWAPI_STARSHIPS = data['next']
            bThereIsMoreData = strURL_SWAPI_STARSHIPS is not None;

        print()
        input('{} ships in total. Hit ENTER to finish.'.format(intAmountOfShips))


App = SW_stops_amount()

if __name__ == '__main__':
    App.run()
