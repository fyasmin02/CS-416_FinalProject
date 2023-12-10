
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
            'csrfmiddlewaretoken': csrf_token
        },
        success: function(data){
            console.log(data);
            const favoriteIcon = $('#favorite-icon-' + id);
            if (data.liked) {
                favoriteIcon.removeClass("bi bi-heart").addClass("bi bi-heart-fill");
            } else {
                favoriteIcon.removeClass("bi bi-heart-fill").addClass("bi bi-heart");
            }

        },
        error: function(error) {
            console.error(error);
            // Handle error (display an error message, etc.)
        }
    })
    }

function updateNote(eventId) {
    const newNote = prompt("Update note:");
    console.log("New note input:", newNote); // Log the input for the new note

    console.log("The raw eventId value is:", eventId); // Add this line to log the raw value
    // Convert eventId to an integer
    // var eventId = $(this).data('event_id');
    // $.ajax({
    //           // type: "POST",
    //           url: "/updateNote/",
    //         success: function (response) {
    //               // Handle success - maybe update the note on the page without a reload
    //               console.log("Note updated successfully:", response); // Log the success response
    //           },
    //           error: function (xhr, status, errorThrown) {
    //               // Handle error
    //               console.error("AJAX request failed with status:", status); // Log the status
    //               console.error("Error thrown:", errorThrown); // Log the error thrown
    //               console.error("Response status:", xhr.status); // Log the HTTP status code
    //               console.error("Response text:", xhr.responseText); // Log the response text
    //          }
    //     });

    //
      if (newNote) {
          console.log("Sending AJAX request to update note for event ID:", eventId); // Log the event ID being sent
          $.ajax({
              type: "POST",
              url: "/updateNote/",
              data: {
                  event_id: eventId,
                  new_note: newNote,
                  csrfmiddlewaretoken: csrf_token
              },
              success: function (response) {
                  // Handle success - maybe update the note on the page without a reload
                  if (response.status === 'success') {
                    var noteId = response.noteid
                      console.log(noteId)
                       $('#note-'+ noteId).text(newNote)
                  }

                  console.log("Note updated successfully:", response); // Log the success response
                                },
              error: function (xhr, status, errorThrown) {
                  // Handle error
                  console.error("AJAX request failed with status:", status); // Log the status
                  console.error("Error thrown:", errorThrown); // Log the error thrown
                  console.error("Response status:", xhr.status); // Log the HTTP status code
                  console.error("Response text:", xhr.responseText); // Log the response text
              }
          });

      }
 }


