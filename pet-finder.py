import requests, csv, json, sys

petsFileName = 'pets.txt'

def searchForDogs():
    data = {
        'key' : sys.argv[1],
        'animal' : 'dog',
        'breed' : 'Australian Shepherd',
        'location' : '55330',
        'count' : 100,
        'format' : 'json'
    }

    request = requests.get('http://api.petfinder.com/pet.find', params=data)
    jsonDict = request.json()

    pets = jsonDict['petfinder']['pets']['pet']

    sortedPets = sorted(pets, key=lambda k: k['id']['$t'])

    return sortedPets

def loadOldDogs():
    try:
        with open(petsFileName, "r") as dogFile:
            return dogFile.read()
    except:
        return ""

def newDogAttachment(name, url, image):
    data = {
        'title' : name,
        'title_link' : url,
        'image_url' : image
    }
    return data

def getDogForId(id, allDogs):
    for dog in allDogs:
        if dog['id']['$t'] == id:
            return dog

def getUrlForDog(dog):
    try:

        #https://www.petfinder.com/dog/lucy-40607778/mn/elk-river/aussie-rescue-of-minnesota-mn108/
        url = "https://www.petfinder.com/dog/{0}-{1}/{2}/{3}/{4}-{5}"
        name = dog['name']['$t'].lower().replace(' ','-')
        dogId = dog['id']['$t']
        state = dog['contact']['state']['$t'].lower().replace(' ','-')
        city = dog['contact']['city']['$t'].lower().replace(' ','-')
        shelterId = dog['shelterId']['$t']
        shelterName = getShelterName(shelterId).lower().replace(' ','-')

        return url.format(name, dogId, state, city, shelterName, shelterId.lower().replace(' ','-'))
    except:
        return ''

def getShelterName(shelterId):
    data = {
        'key' : sys.argv[1],
        'id' : shelterId.strip(),
        'format': 'json'
    }

    request = requests.get('http://api.petfinder.com/shelter.get', params=data)
    jsonDict = request.json()

    return jsonDict['petfinder']['shelter']['name']['$t']

sortedDogs = searchForDogs()
newIds = list(map(lambda dog: dog['id']['$t'], sortedDogs))

oldDogs = loadOldDogs().splitlines()

diffDogs = [dog for dog in newIds if dog not in oldDogs]

if len(diffDogs) != 0:

    data = {'text' : '@here new dogs!'}
    requests.post(sys.argv[2], json=data)

    for newDog in diffDogs:
        dog = getDogForId(newDog, sortedDogs)
        data = {}
        attachments = []
        data['attachments'] = attachments

        attachments.append(newDogAttachment(dog['name']['$t'], getUrlForDog(dog), dog['media']['photos']['photo'][2]['$t']))

        requests.post(sys.argv[2], json=data)


with open(petsFileName, "w") as dogFile:
    dogFile.write("\n".join(newIds))