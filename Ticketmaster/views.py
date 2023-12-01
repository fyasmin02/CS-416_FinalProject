import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Userprofile, EventHistory, EventFavorite
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def index(request):
    if request.method == 'POST':
        # search_term = "dance"
        search_term = request.POST.get('search_term')
        # location = "boston"
        location = request.POST.get('location')

        if search_term.strip() == '' and location.strip() == '':
            return render(request, 'ticketmaster.html',
                          {'errors': True, 'message': 'Search and city term cannot be empty. Please enter both terms.'})
        elif search_term.strip() == '':
            return render(request, 'ticketmaster.html',
                          {'errors': True, 'message': 'Search term cannot be empty. Please enter a search term.'})
        elif location.strip() == '':
            return render(request, 'ticketmaster.html',
                          {'errors': True, 'message': 'City term cannot be empty. Please enter a city term.'})

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
                event_id = event['id']
                name = event['name']
                venue = event['_embedded']['venues'][0]['name']
                address = event['_embedded']['venues'][0]['address']["line1"]
                city = event['_embedded']['venues'][0]['city']['name']
                state = event['_embedded']['venues'][0]['state']['name']
                startDate = event['dates']['start']['dateTime']
                startTime = event['dates']['start']['localTime']
                ticketLink = event['url']
                img = event['images'][0]['url']

                formatted_date = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S%z").strftime("%b %d, %Y")
                formatted_time = datetime.strptime(startTime, "%H:%M:%S").strftime("%I:%M %p")

                event_details = {
                    'id': event_id,
                    'name': name,
                    'venue': venue,
                    'address': address,
                    'city': city,
                    'state': state,
                    'startDate': formatted_date,
                    'startTime': formatted_time,
                    'ticketLink': ticketLink,
                    'img': img
                }
                event_list.append(event_details)

                # EventHistory.objects.create(
                #     eventid=event_id,
                #     name=name,
                #     venue=venue,
                #     address=address,
                #     city=city,
                #     state=state,
                #     start_date=formatted_date,
                #     start_time=formattedma_time,
                #     ticket_link=ticketLink,
                #     image_url=img
                # )

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


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Userprofile.objects.filter(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You Must Be Logged In"))
        return redirect('ticketmaster')


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ticketmaster')
        else:
            messages.success(request, ("There was an error. Try again!"))
            return redirect('login')

    else:
        return render(request, "login.html", {})


def log_out(request):
    logout(request)
    return redirect('ticketmaster')

@csrf_exempt
@require_POST
def addEventFavorite(request):
    id = request.POST.get('event_id')
    likedOrUnliked = request.POST.get('likedOrUnliked')
    print(id)
    response_data = {'message': 'Data received and processed successfully!'}
    try:
        apikey = "1FPse6gUOjUlhYtMUbdEG6Wz5GsGmj3v"
        url = f'https://app.ticketmaster.com/discovery/v2/events/{id}?apikey={apikey}'
        response = requests.get(url)
        event = response.json()
        id = event['id']
        name = event['name']
        venue = event['_embedded']['venues'][0]['name']
        address = event['_embedded']['venues'][0]['address']["line1"]
        city = event['_embedded']['venues'][0]['city']['name']
        state = event['_embedded']['venues'][0]['state']['name']
        startDate = event['dates']['start']['dateTime']
        startTime = event['dates']['start']['localTime']
        ticketLink = event['url']
        img = event['images'][0]['url']

        formatted_date = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S%z").strftime("%b %d, %Y")
        formatted_time = datetime.strptime(startTime, "%H:%M:%S").strftime("%I:%M %p")

        if(likedOrUnliked == "unliked"):
            eventEntry = EventFavorite.objects.get(eventid=id)
            eventEntry.delete()
        else:
            EventFavorite.objects.create(
                eventid=id,
                name=name,
                venue=venue,
                address=address,
                city=city,
                state=state,
                start_date=formatted_date,
                start_time=formatted_time,
                ticket_link=ticketLink,
                image_url=img
            )

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


    return JsonResponse(response_data)

