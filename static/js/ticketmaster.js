
function convertDate(date) {
    //const date = "2023-11-27T00:30:00Z"
    return new Date(date).toDateString();
}

function convertTime(time) {
    const options = {hour: 'numeric', minute: '2-digit', hour12: true};
    return new Date(`1970-01-01T${time}Z`).toLocaleTimeString('en-US', options);
}

function highQualityImage(images) {
    let highestWidth = 0;
    let highestHeight = 0;
    let highQualityImageUrl = "";

    images.forEach(image => {
        if (image.width > highestWidth || (image.width === highestWidth && image.height > highestHeight)) {
            highestWidth = image.width;
            highestHeight = image.height;
            highQualityImageUrl = image.url;
        }
    });
    console.log("Highest Width:", highestWidth);
    console.log("Highest Height:", highestHeight);
    console.log("Highest Image URL:", highQualityImageUrl);
    return highQualityImageUrl;
}

function likeEvent(id) {
    console.log(id);
    $.ajax({
        type: "POST",
        url: "/addEventFavorite/",
        data: {
            'event_id': id,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(data){
            console.log("success" + id)
        },
        error: function(error) {
            console.error(error);
            // Handle error (display an error message, etc.)
        }
    })
    }

        //
        //
        // $(document).ready(function () {
        //     $('.btn-primary').on('click', function () {
        //         const searchTerm = $('input[name=search_term]').val();
        //         const location = $('input[name=location]').val();
        //         const corsAnywhereURL = 'https://cors-anywhere.herokuapp.com/';
        //         const apikey = "1FPse6gUOjUlhYtMUbdEG6Wz5GsGmj3v";
        //
        //         if (searchTerm.trim() === '' && location.trim() === '') {
        //             $('#alert').text('Search and city term cannot be empty. Please enter both terms').removeClass('d-none');
        //         } else if (searchTerm.trim() === '') {
        //             $('#alert').text('Search term cannot be empty. Please enter a search term').removeClass('d-none');
        //         } else if (location.trim() === '') {
        //             $('#alert').text('City term cannot be empty. Please enter a city term').removeClass('d-none');
        //         } else {
        //             $('#alert').addClass('d-none');
        //             console.log('Genre/Artist/Event:', searchTerm);
        //             console.log('City:', location);
        //         }
        //
        //         $('#results').empty();
        //
        //         $.ajax({
        //             url: "https://app.ticketmaster.com/discovery/v2/events",
        //             dataType: "json",
        //             data: {
        //                 'classificationName': searchTerm,
        //                 'city': location,
        //                 'apikey': apikey,
        //                 'sort': 'date,asc'
        //             },
        //             method: "GET",
        //
        //
        //             success: function (data) {
        //                 const listOfEvents = data.page.totalElements;
        //                 if (listOfEvents === 0) {
        //                     $('#resultContainer').show();
        //                     $('#results').append('<h5>Sorry...No results were found for the entered term and city!</h5>');
        //                 } else {
        //
        //                 }
        //                 console.log(listOfEvents);
        //                 console.log(data);
        //                 const totalEvents = data._embedded.events.length;
        //                 console.log('Total: ' + totalEvents);
        //
        //                 if (listOfEvents > 0) {
        //                     if (searchTerm.trim() === '' || location.trim() === '') {
        //                         $('#resultContainer').hide();
        //                     } else {
        //                         $('#resultContainer').show();
        //                     }
        //                     $('#results').empty().append(`<h5>${totalEvents} events found </h5>`)
        //                     $.each(data._embedded.events, function (i, event) {
        //                         const eventName = event.name;
        //                         console.log(eventName);
        //                         const img = highQualityImage(event.images);
        //                         console.log(img);
        //                         const startDate = convertDate(event.dates.start.dateTime);
        //                         console.log(startDate);
        //                         const startTime = convertTime(event.dates.start.localTime);
        //                         console.log(startTime);
        //                         const venueName = event._embedded.venues[0].name;
        //                         console.log(venueName);
        //                         const city = event._embedded.venues[0].city.name;
        //                         console.log(city);
        //                         const state = event._embedded.venues[0].state.name;
        //                         console.log(state);
        //                         const address = event._embedded.venues[0].address.line1;
        //                         console.log(address);
        //                         const ticketLink = event.url;
        //                         console.log(ticketLink);
        //
        //
        //                         $('#results').append('' + ' <div class="card shadow p-2 mb-3">\n' +
        //                             '                    <div class="row g-0 align-items-center">\n' +
        //                             '                        <div class="col-md-4 ">\n' +
        //                             `                            <img src="${img}" class="img-fluid rounded-start" alt="...">\n` +
        //                             '                        </div>\n' +
        //                             '                        <div class="col-md-8 ">\n' +
        //                             '                            <div class="card-body">\n' +
        //                             '                                <div class="row g-0 pb-2 ">\n' +
        //                             '                                    <div class="col-6 col-sm-6 ">\n' +
        //                             `                                        <h5 class="card-title">${eventName}</h5>\n` +
        //                             `                                        <p class="card-text">${venueName}</p>\n` +
        //                             `                                        <p class="card-text"><small class="text-body-secondary">${address} <br>${city},${state}</small></p>\n` +
        //                             '                                    </div>\n' +
        //                             '                                    <div class="col-6 col-sm-6  text-end">\n' +
        //                             `                                         <p class="card-text">${startDate}</p>\n` +
        //                             `                                         <p class="card-text">${startTime}</p>\n` +
        //                             '                                        </div>\n' +
        //                             '\n' +
        //                             '                                    </div>\n' +
        //                             `                                 <a href="${ticketLink}"><button type="button" class="btn btn-primary">Find tickets</button></a>\n` +
        //                             '\n' +
        //                             '                                </div>\n' +
        //                             '                            </div>\n' +
        //                             '                        </div>\n' +
        //                             '                    </div>');
        //
        //
        //                     });
        //                 } else {
        //                     /*$('#resultContainer').show();
        //                     console.log('bingo')
        //                     $('#results').append('<h5>Sorry...No results were found for the entered term and city!</h5>');*/
        //                     //$('#results').append('<h5>No results were found!</h5>');
        //                 }
        //
        //             },
        //
        //         });
        //     })
        // });


