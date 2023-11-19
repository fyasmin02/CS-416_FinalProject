import requests
import time
from django.shortcuts import render


def search(request):
    searchTerm = "dance"
    city = "boston"
    apikey = "1FPse6gUOjUlhYtMUbdEG6Wz5GsGmj3v"
    url = "https://app.ticketmaster.com/discovery/v2/events"

    params = {
        'classificationName': searchTerm,
        'city': city,
        'apikey': apikey,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
    events = data['_embedded']['events']
    event_list = []

    for event in events:
        name = event['name']
        venue = event['_embedded']['venues'][0]['name']
        address = event['_embedded']['venues'][0]['address']["line1"]
        city = event['_embedded']['venues'][0]['city']['name']
        state = event['_embedded']['venues'][0]['state']['name']
        startDate = event['dates']['start']['dateTime']
        startTime = event['dates']['start']['localTime']
        ticketLink = event['url']
        img = event['images'][0]['url']

        event_details = {
            'name': name,
            'venue': venue,
            'address': address,
            'city': city,
            'state': state,
            'startDate': startDate,
            'startTime': startTime,
            'ticketLink': ticketLink,
            'img': img
        }
        event_list.append(event_details)
        context = {'events':event_list}

    return render(request, 'ticketmaster.html', context)


