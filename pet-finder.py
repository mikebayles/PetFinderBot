from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')


def search_for_dogs():
    data = {
        'key': os.environ['api_key'],
        'animal': 'dog',
        'breed': os.environ['breed'],
        'location': os.environ['zip'],
        'count': 100,
        'format': 'json',
        'output': 'basic'
    }

    request = requests.get('http://api.petfinder.com/pet.find', params=data)
    json_dict = request.json()

    pets = json_dict['petfinder']['pets']['pet']

    return pets


def new_dog_attachment(name, url, image):
    data = {
        'title': name,
        'title_link': url,
        'image_url': image
    }
    return data


def get_dog_for_id(dog_id, all_dogs):
    for dog in all_dogs:
        if dog['id']['$t'] == dog_id:
            return dog


def get_url_for_dog(dog):
    url = "https://www.petfinder.com/petdetail/{0}"
    dog_id = dog['id']['$t']

    return url.format(dog_id)


def get_photo_for_dog(dog):
    sizes = {
        'x': [],
        't': [],
        'pn': [],
        'pnt': [],
        'fpm': []
    }

    try:
        for photo in dog['media']['photos']['photo']:
            size = photo['@size']
            sizes[size].append(photo['$t'])

        for key in sorted(sizes, reverse=True):
            if len(sizes[key]) > 0:
                return sizes[key][0]

    except Exception as e:
        print('Could not get photo', dog, e)

    return None


def get_new_dogs_with_pics(dogs):
    new_dogs = []
    table = dynamodb.Table('Pets')

    for dog in dogs:
        try:
            photo = get_photo_for_dog(dog)
            if not photo:
                continue

            table.put_item(
                Item={
                    'id': dog['id']['$t'],
                },
                ConditionExpression=Attr('id').not_exists())

            new_dogs.append((dog, photo))

        except ClientError as e:
            pass

    return new_dogs


def main():
    all_dogs = search_for_dogs()
    new_dogs = get_new_dogs_with_pics(all_dogs)

    slack_hook = os.environ['slack_hook']

    data = {'text': '<!here> new dogs!'}
    attachments = []
    data['attachments'] = attachments

    for (dog, photo) in new_dogs:
        attachments.append(new_dog_attachment(dog['name']['$t'], get_url_for_dog(dog), photo))

    if len(attachments) > 0:
        requests.post(slack_hook, json=data)


if __name__ == "__main__":
    main()
