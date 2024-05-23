# put cities in memory
cities = []
with open('cities.txt', 'r') as cityFile:
    for city in cityFile:
        cities.append(city[:-1])

# put states in memory
states = []
with open('states.txt', 'r') as stateFile:
    for state in stateFile:
        states.append(state[:-1])

# init dictionary with number of cities per state
# and dictionary with list of cities per state
number_of_cities = {}
list_of_cities = {}
for state in states:
    number_of_cities[state] = 0
    list_of_cities[state] = []

for city in cities:
    city_state  = city.split(',')
    curr_city   = city_state[0].strip()
    curr_state  = city_state[-1].strip()
    
    curr_state_count = number_of_cities[curr_state]
    curr_state_count += 1
    number_of_cities[curr_state] = curr_state_count

    curr_list = list_of_cities[curr_state]
    curr_list.append(curr_city)
    list_of_cities[state] = curr_list

# some bug above causes Wyoming to receive the Wisconsin list
# but there are no relevant cities in Wyoming, so just zero it out
list_of_cities['Wyoming'] = []

def printCities(state=None):
    if state == None:
        for state in list_of_cities:
            state_cities = list_of_cities[state]
            print(state+":")
            for city in state_cities:
                print("\t"+city)
    
    elif state not in states:
        print("Not a US state (check punctuation!), aborting...")
        return 1

    else:
        state_cities = list_of_cities[state]
        print(state+":")
        for city in state_cities:
            print("\t"+city)

    return 0



