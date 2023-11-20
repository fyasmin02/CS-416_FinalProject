import requests
from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        # search_term = "dance"
        search_term = request.POST.get('search_term')
        # location = "boston"
        location = request.POST.get('location')
        print(search_term)
        print(location)

        if not search_term or not location:
            messages.info(request, 'Both number of users and gender are required fields.')
            return redirect('search-index')

        data = get_data(search_term, location)

        if data is None:
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            return redirect('search-index')
        else:
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
            context = {'events': event_list}
            return render(request, 'ticketmaster.html', context)

    return render(request, 'ticketmaster.html')


def get_data(search_term, location):
    try:
        apikey = "1FPse6gUOjUlhYtMUbdEG6Wz5GsGmj3v"
        url = "https://app.ticketmaster.com/discovery/v2/events"

        params = {
            'classificationName': search_term,
            'city': location,
            'apikey': apikey,
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None
