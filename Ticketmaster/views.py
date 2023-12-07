import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Userprofile, EventHistory, EventFavorite, NoteHistory
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

                try:
                    # Try to get the EventFavorite with the specified event_id
                    event_favorite = EventFavorite.objects.get(eventid=event_id)
                    # If the record exists, set inFavorite to "bi-heart-fill"
                    inFavorite = "bi-heart-fill"
                except EventFavorite.DoesNotExist:
                    # If the record does not exist, set inFavorite to "bi-heart"
                    inFavorite = "bi-heart"

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
                    'inFavorite': inFavorite,
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

@csrf_exempt
def addEventFavorite(request):
    event_id = request.POST.get('event_id')
    likedOrUnliked = request.POST.get('likedOrUnliked')
    response_data = {'message': 'Data received and processed successfully!'}
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


def favoritesTab(request):
    if request.user.is_authenticated:
        liked_events = EventFavorite.objects.all()
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
                'message': 'something went wrong'
            }
        )


# second attempt
# def add_notes(request):
#     if request.method == "POST":
#         event_id = request.POST.get('event_id')
#         message = request.POST.get('message')
#         return render(request, "notes.html")
#     else:
#         return redirect(request, "ticketmaster.html")

# first attempt
# def add_notes(request):
#     if request.method == 'POST':
#         event_id = request.POST.get('event_id')
#         note_text = request.POST.get('message')
#
#         try:
#             # Convert the event_id to an integer
#             event_id = event_id
#             # Find the event object associated with the event_id
#             event = get_object_or_404(EventHistory, pk=event_id)
#             # Create a new note instance and save it
#             note = NoteHistory.objects.create(event=event, message=note_text)
#
#             # Prepare the response data
#             response_data = {
#                 'status': 'success',
#                 'note_id': note.id,
#                 'message': 'Note added successfully',
#             }
#
#             return JsonResponse(response_data)
#         except (ValueError, EventHistory.DoesNotExist) as e:
#             print(f"Error: {e}")
#             return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
#
#

def notes(request):
    if request.user.is_authenticated:
        noted_events = NoteHistory.objects.all()
        context = {'noted_events': noted_events}
        return render(request, "notes.html", context)
    else:
        messages.success(request, "You Must Be Logged In")
        return redirect('ticketmaster')


# def add_notes(request):
#     event = request.POST.get('event_id')
#     note = request.POST.get('note')
#     print('eventid ', event)
#     print('note ',note)
#     response_data = {'message': 'Data received and processed successfully!'}
#     form = NoteForm(request.POST or None)
#
#     if form.is_valid():
#         form.save()
#
#         return redirect('views_notes')
#
#     return render(request, 'notes.html', {'form': form})
#     # Only allow POST requests
#     if request.method == 'POST':
#         # Extract data from the request
#         event_id = request.POST.get('eventid')
#         note = request.POST.get('noted')
#
#         # Find the event object associated with the event_id
#         event = get_object_or_404(Event, pk=event_id)
#
#         # Create a new note instance and save it
#         note = Note.objects.create(
#             eventid=id,
#             name=name,
#             message=message,
#             venue=venue,
#             address=address,
#             city=city,
#             state=state,
#             start_date=formatted_date,
#             start_time=formatted_time,
#             ticket_link=ticketLink,
#             image_url=img
#         )
#
#         # Prepare the response data
#         response_data = {
#             'status': 'success',
#             'note_id': note.id,  # You can send back the ID of the created note
#             'liked': True,  # Or any other data that your JavaScript expects
#         }
#
#         return JsonResponse(response_data)
#
#     else:
#         # If not a POST request, return an error response
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)  #


# For updating note
# def update_note(request, id):
#     note_events = NoteHistory.objects.get(id=id)
#     form = NoteForm(request.POST or None, instance=note_events)
#
#     if form.is_valid():
#         form.save()
#         return redirect('view_notes')
#
#     return render(request, 'note-form.html', {'form':form})
#
# # For deleting note
# def delete_note(request):
#     note_events = NoteHistory.objects.get(id=id)
#     if request.method == 'POST':
#         note_events.delete()
#         return redirect('view_notes')
#     return render(request,'delete-confirm.html', {'note_events':note_events})