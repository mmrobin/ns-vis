from bs4 import BeautifulSoup
import requests
import re

# list of US states -- used to search with BeautifulSoup
'''
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 
          'California', 'Colorado', 'Connecticut', 'Delaware',
          'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois',
          'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
          'Maine', 'Maryland', 'Massachusetts', 'Michigan',
          'Minnesota', 'Mississippi', 'Missouri', 'Montana',
          'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
          'New Mexico', 'New York', 'North Carolina',
          'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
          'Pennsylvania', 'Rhode Island', 'South Carolina',
          'South Dakota', 'Tennessee', 'Texas', 'Utah',
          'Vermont', 'Virginia', 'Washington', 'West Virginia',
          'Wisconsin', 'Wyoming']

with open('states.txt', 'w') as file:
    for state in states:
        file.write(f'{state}\n')
'''

# create the states list
# it is better to have this as a separate file
stateFile = open('states.txt', 'r')
states = []
for state in stateFile.readlines():
    states.append(state[:-1])
stateFile.close()

# print(len(states))

# download Wikipedia article
# page = requests.get("https://en.wikipedia.org/wiki/List_of_U.S._places_named_after_non-U.S._places")

# saved local version of Wikipedia page
# (to be able to work locally and not scrape them every time)
page = open("page.html")
htmlContent = BeautifulSoup(page, 'html.parser')

# print(page.status_code)
# print(page.content)
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

'''
with open('page.html', 'w') as file:
    file.write(str(soup))
'''

html = str(htmlContent)
tableList = html.split('<h2>')

# print(tableList[9].split('"'))
# print()
# tableList[74] is United Kingdom; handle this case separately
# tableList[9] is Belgium, which is a good reference point

####    NON-WORKING FUNCTIONS    ####

# send elements of the tableList to this function
def digest(table):
    
    # don't look at me
    country = table.split('id')[1].split('>')[1].split('<')[0]    
    print(f"Country: {country}")

    # check that country is being processed correctly
    if country != 'mw-headline':
        pass
    else:
        print('####    Used 5    ####')
        country = table.split('"')[5]


    namesakes = {}
    # find country's cities in data
    '''
    data = table.split(']')[1].split('title=')
    namesake = data[1].split('>')[0][1:-1]
    '''

    #data = table.split('')

    return 0

print(digest(tableList[14]))

####    WORKING FUNCTIONS    ####

# produces list of US markers per-state
def findCities(state):
    # nasty regex business
    stateString = ", "+state
    cities = htmlContent.find_all(string=re.compile(stateString+"$"))
    
    cities = list(set(cities)) # remove duplicate entries
    cities.sort() # put in alphabetical order
    
    # this string sometimes occurs in the html
    # if it does, remove it
    if stateString in cities:
        cities.remove(stateString)
    
    print(f"Found {len(cities)} cities in {state}")
    
    for city in cities:
        # print(city)
        pass

    return cities

####    COUNT US PLACES    ####

count = 0
best = 0
bestState = 0
allCities = []
for state in states:
    cities = findCities(state)
    stateCount = len(cities)
    # add to the total count of cities found
    count += stateCount
    if stateCount > best:
        best = stateCount
        bestState = state
    for city in cities:
        allCities.append(city)

print(f"Found {count} US places named after non-US places")
print(f"{bestState} has the most, with {best}")

# used to write cities.txt
# this file contains all US cities found in the Wikipedia page
'''
with open('cities.txt', 'w') as cityFile:
    for city in allCities:
        cityFile.write(city+"\n")
'''
# there are 1299 cities (need to remove a few outliers)