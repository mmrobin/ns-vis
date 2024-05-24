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

# write countries dictionary
# associates to each country a soup object
html = str(htmlContent)
tableList = html.split('<h2>')
countries = {}
for table in tableList[1:-3]:
    soup = BeautifulSoup(table, 'html.parser')
    country = soup.find("span")["id"]
    if ".28" in country:
        cutoff = country.index("_")
        country = country[:cutoff]
    countries[country] = soup




# print(tableList[9].split('"'))
# print()
# tableList[74] is United Kingdom; handle this case separately
# tableList[9] is Belgium, which is a good reference point

####    NON-WORKING FUNCTIONS    ####

# send elements of the tableList to this function
'''
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
    
    #data = table.split(']')[1].split('title=')
    #namesake = data[1].split('>')[0][1:-1]
    

    #data = table.split('')

    return 0
'''
# print(digest(tableList[14]))


def digest(country):
    # input: an element of the tableList
    if country not in list(countries.keys()):
        print(f"Could not find {country} in list, aborting...")
        return 1
    else:
        pass

    # retrieve the parsed bs4 object from the countries dict
    content = countries[country]

    # find all <tr> tags
    # <tr> and </tr> delimit namesake cities
    tr_tags = content.find_all('tr')[1:]
    tr_ns = {}
    for block in tr_tags:
        try:
            # the html tag <td> my have an attribute 'rowspan'
            # which indicates how many ciites are associated to a namesake
            tag = block.td                          # first td tag is namesake
            rowspan = int(tag.attrs['rowspan'])     # count US cities
        except:
            # if 'rowspan' is not specified, there is one namesake
            rowspan = 1
        # block.td is the first <td> tag
        namesake = block.td.get_text()
        if "\n" in namesake:
            namesake = namesake[:-2]

        for td in block:
            # print(td.get_text())
            pass

        # print(f"NEW BLOCK: {namesake}, Rowspan = {rowspan}")
        tr_ns[namesake] = rowspan

    # print(tr_ns)
    ns = list(tr_ns.keys())
    ns_trimmed = ns.copy()
    for i in range(0, len(ns)):
        namesake = ns[i]
        rs = int(tr_ns[namesake])
        # print(f"{namesake}, {rs}")
        if rs == 1:
            pass
        else:
            children = ns[i+1:i+rs]
            # print(children)
            for child in children:
                ns_trimmed.remove(child)

    rs_trimmed = []
    for namesake in ns_trimmed:
        rs_trimmed.append(int(tr_ns[namesake]))
    # print(rs_trimmed)

    tr_ns_trimmed = {ns:rs for (ns,rs) in zip(ns_trimmed, rs_trimmed)}
    print(tr_ns_trimmed)

    # dictionary of the form namesake: [US place(s)]
    ns_us = {}
    
    for i in range(len(ns_trimmed)):
        namesake = ns_trimmed[i]
        rowspan = tr_ns_trimmed[namesake]
        offset = 0
        for j in range(0, i):
            offset += tr_ns_trimmed[ns_trimmed[j]]
        block = tr_tags[offset:offset+rowspan]
        

        matches = []
        for line in block:
            names = line.find_all(string=re.compile(".*, .*"))

            for name in names:
                if name[0] == ',':
                    pass

            # print(names)
            if "," in namesake:
                if len(names) > 1:
                    matches.append(names[1])
                else:
                    matches.append(names[0])
            else:
                matches.append(names[0])

        print(f"{namesake}: rowspan = {rowspan}\n{matches}")





























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
'''
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
'''

# used to write cities.txt
# this file contains all US cities found in the Wikipedia page
'''
with open('cities.txt', 'w') as cityFile:
    for city in allCities:
        cityFile.write(city+"\n")
'''
# there are 1299 cities (need to remove a few outliers)


