
import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for item in data:
        if actor_id_1 in item[:2] and actor_id_2 in item[:2]:
            return True
    return False

def get_actors_with_bacon_number(data, n):
    newData = {}
    #Creating a dictionary with actor id as key, and set of all actors that actor has acted with as value
    for i in range(len(data)):
        if data[i][0] in newData:
            newData[data[i][0]].add(data[i][1])
        else:
            newData[data[i][0]] = {data[i][1]}
        if data[i][1] in newData:
            newData[data[i][1]].add(data[i][0])
        else:
            newData[data[i][1]] = {data[i][0]}

    count = n
    currentSet = {4724} #Holds all actors with bacon number count
    cumulativeSet = {4724} #Holds all actors with bacon number <= count
    while count > 0 and len(currentSet)>0:
        tempSet = set() #Will hold all actors in a movie with each actor in currentSet, including actors in currentSet
        for actor in currentSet: #Iterates through all actors in currentSet
            for otherActor in newData[actor]:
                tempSet.add(otherActor) #adding all actors that this actor has acted with to tempSet
        currentSet = tempSet - cumulativeSet #currentSet filters tempSet to not include any actors in cumulativeSet
        count -= 1
        cumulativeSet = tempSet | cumulativeSet #tempSet added to cumulativeSet
    return currentSet

def get_bacon_path(data, actor_id):
    newData = {}
    #Creating a dictionary with actor id as key, and set of all actors that actor has acted with as value
    for i in range(len(data)):
        if data[i][0] in newData:
            newData[data[i][0]].add(data[i][1])
        else:
            newData[data[i][0]] = {data[i][1]}
        if data[i][1] in newData:
            newData[data[i][1]].add(data[i][0])
        else:
            newData[data[i][1]] = {data[i][0]}

    #Implementing BFS Algorithm

    bacon = 4724 #Initial starting node
    toCheck = [[bacon]] #List of paths to be checked
    checked = set() #Nodes that have already been checked
    currentElem = 0 #Index in toCheck that we are currently on

    if bacon == actor_id: #Checks if looking for bacon path of Kevin Bacon
        return [bacon]

    while currentElem < len(toCheck): #While there are still paths to be checked
        currentPath = toCheck[currentElem]
        currentActor = currentPath[-1]

        if currentActor not in checked:
            checked.add(currentActor)
            for otherActor in newData[currentActor]:
                if otherActor not in checked:
                    newPath = currentPath[:]
                    newPath.append(otherActor) #New path is old path + current actor
                    toCheck.append(newPath) #Appending new path to be checked

                    if otherActor == actor_id:
                        return newPath

        currentElem += 1
        
    return None

def get_path(data, actor_id_1, actor_id_2):
    newData = {}
    #Creating a dictionary with actor id as key, and set of all actors that actor has acted with as value
    for i in range(len(data)):
        if data[i][0] in newData:
            newData[data[i][0]].add(data[i][1])
        else:
            newData[data[i][0]] = {data[i][1]}
        if data[i][1] in newData:
            newData[data[i][1]].add(data[i][0])
        else:
            newData[data[i][1]] = {data[i][0]}

    #Implementing BFS Algorithm
    toCheck = [[actor_id_1]] #List of paths to be checked
    checked = set() #Nodes that have already been checked
    currentElem = 0 #Index in toCheck that we are currently on

    if actor_id_1 == actor_id_2: #Checks if looking for bacon path of Kevin Bacon
        return [actor_id_1]

    while currentElem < len(toCheck): #While there are still paths to be checked
        currentPath = toCheck[currentElem]
        currentActor = currentPath[-1]

        if currentActor not in checked:
            checked.add(currentActor)
            for otherActor in newData[currentActor]:
                if otherActor not in checked:
                    newPath = currentPath[:]
                    newPath.append(otherActor) #New path is old path + current actor
                    toCheck.append(newPath) #Appending new path to be checked

                    if otherActor == actor_id_2:
                        return newPath

        currentElem += 1

    return None

def get_movies(data, actor_id_1, actor_id_2):
    path = get_path(data, actor_id_1, actor_id_2)
    newData = {}
    for i in range(len(data)):
        if data[i][2] in newData:
            newData[data[i][2]].add(data[i][0])
            newData[data[i][2]].add(data[i][1])
        else:
            newData[data[i][2]] = {data[i][0],data[i][1]}

    movies = []
    for i in range(len(path)-1):
        for movie in newData:
            if {path[i],path[i+1]}.issubset(newData[movie]):
                movies.append(movie)
                break;
    return movies

if __name__ == '__main__':
    with open('resources/small.json') as f:
        smalldb = json.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
