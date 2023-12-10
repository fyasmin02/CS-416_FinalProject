import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Userprofile, EventHistory, EventFavorite, NoteHistory
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import registerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms



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

            #EventFavorite.objects.all().delete()


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

                if request.user.is_authenticated:
                    event_favorite_count = EventFavorite.objects.filter(user=request.user, eventid=event_id).count()  # added for multiuser
                else:
                    event_favorite_count = EventFavorite.objects.filter(eventid=event_id).count()
                favorite_status = True
                if event_favorite_count == 0:
                    favorite_status = False

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
                    'img': img,
                    'favorite_status': favorite_status,
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
                #     start_time=formatted_time,
                #     ticket_link=ticketLink,
                #     image_url=img,
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


def get_event_from_id(event_id):
    try:
        apikey = "1FPse6gUOjUlhYtMUbdEG6Wz5GsGmj3v"
        url = f'https://app.ticketmaster.com/discovery/v2/events/{event_id}?apikey={apikey}'
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

        event_data = {
                'eventid': id,
                'name': name,
                'venue': venue,
                'address': address,
                'city': city,
                'state': state,
                'start_date': formatted_date,
                'start_time': formatted_time,
                'ticket_link': ticketLink,
                'image_url': img
        }

        return event_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None



def addEventFavorite(request):
    #if request.method == 'POST':
    if request.method == 'POST' and request.user.is_authenticated:  # added for multiuser
        event_id = request.POST.get('event_id')

        print(event_id)


        #EventFavorite.objects.all().delete()

        response_data = {'message': 'Data received and processed successfully!'}

        liked = True

        event_data = get_event_from_id(event_id)

        event_object, created = EventFavorite.objects.get_or_create(
            user=request.user,  # added for multiuser
            eventid=event_data['eventid'],
            name=event_data['name'],
            venue=event_data['venue'],
            address=event_data['address'],
            city=event_data['city'],
            state=event_data['state'],
            start_date=event_data['start_date'],
            start_time=event_data['start_time'],
            ticket_link=event_data['ticket_link'],
            image_url=event_data['image_url'],
            liked=liked
        )

        print('created status:', created)

        if not created:
            liked = False
            event_object.delete()  # added for multiuser
            # EventFavorite.objects.get(eventid=event_id).delete()

        return JsonResponse(
            {
                'liked': liked
            }
        )
    else:
        return JsonResponse(
            {
                'message': 'Something went wrong'
            }
        )


def favoritesTab(request):
    if request.user.is_authenticated:
        # liked_events = EventFavorite.objects.all()
        liked_events = EventFavorite.objects.filter(user=request.user)  # added for multiuser
        context = {'liked_events': liked_events}
        return render(request, "favoritesTab.html", context)
    else:
        messages.success(request, "You Must Be Logged In")
        return redirect('ticketmaster')

# third attempt
def add_notes(request):
    if request.method == "POST":
        #EventHistory.objects.all().delete()
        note_text = request.POST['message']
        event_id = request.POST['event_id']

        print(note_text)
        print(event_id)

        event_data = get_event_from_id(event_id)

        event_object, created = EventHistory.objects.get_or_create(
            eventid=event_data['eventid'],
            name=event_data['name'],
            venue=event_data['venue'],
            address=event_data['address'],
            city=event_data['city'],
            state=event_data['state'],
            start_date=event_data['start_date'],
            start_time=event_data['start_time'],
            ticket_link=event_data['ticket_link'],
            image_url=event_data['image_url']
        )


        # probably need to modify this
        #event = get_object_or_404(EventHistory, eventid=event_id)
        if created:
            NoteHistory.objects.create(event=event_object, message=note_text)

        #put an else condition so that you can update the message if it already exist

        return JsonResponse(
            {
                'added': True,
                'message': 'Note has added'
            }
        )  # redirecting to notes.html after adding the notes
    else:
        return JsonResponse(
            {
                'message': 'Something went wrong'
            }
        )


# def delete_notes(request):
#     if request.method == 'POST':
#         event_id = request.POST.get('event_id')
#
#         try:
#             event = NoteHistory.objects.get(eventid=event_id)
#             event.delete()
#             deleted = True
#         except NoteHistory.DoesNotExist:
#             deleted = False
#
#         return JsonResponse({'deleted': deleted})
#     else:
#         return JsonResponse({'message': 'Invalid request method'})


def notes(request):
    if request.user.is_authenticated:
        noted_events = NoteHistory.objects.all()
        context = {'noted_events': noted_events}
        return render(request, "notes.html", context)
    else:
        messages.success(request, "You Must Be Logged In")
        return redirect('ticketmaster')


def register(request):
    form = registerForm()
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # User log in
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('ticketmaster')
    return render(request,"register.html", {'form': form})