
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


