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
        url = "https://www.petfinder.com/petdetail/{0}"
        dogId = dog['id']['$t']

        return url.format(dogId)
    except:
        return ''

    request = requests.get('http://api.petfinder.com/shelter.get', params=data)
    jsonDict = request.json()

    return jsonDict['petfinder']['shelter']['name']['$t']

def getPhotoForDog(dog):
    try:
        return dog['media']['photos']['photo'][2]['$t']
    except:
        return ''

sortedDogs = searchForDogs()
newIds = list(map(lambda dog: dog['id']['$t'], sortedDogs))

oldDogs = loadOldDogs().splitlines()

diffDogs = [dog for dog in newIds if dog not in oldDogs]

if len(diffDogs) != 0:

    data = {'text' : '<!here> new dogs!'}
    requests.post(sys.argv[2], json=data)

    for newDog in diffDogs:
        dog = getDogForId(newDog, sortedDogs)
        data = {}
        attachments = []
        data['attachments'] = attachments

        attachments.append(newDogAttachment(dog['name']['$t'], getUrlForDog(dog), getPhotoForDog(dog)))

        requests.post(sys.argv[2], json=data)


with open(petsFileName, "w") as dogFile:    
    dogFile.write("\n".join(list(set().union(newIds,oldDogs))))
