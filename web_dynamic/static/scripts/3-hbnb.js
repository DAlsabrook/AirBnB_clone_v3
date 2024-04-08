$(document).ready(function () {
    $(document).on('change', "input[type='checkbox']", function () {
        const checkedList = [];
        // Iterate through each checkbox
        $('input[type="checkbox"]').each(function () {
            // Add all checked names to the list
            if ($(this).is(':checked')) {
                checkedList.push($(this).attr('data-name'));
            }
        });
        if (checkedList.length === 0) {
            // If nothing is checked add the nbsp back
            $('.checkedList').html('&nbsp;');
        } else {
            // Update the h4 tag with the list of checked amenities
            $('.checkedList').text(checkedList.join(', '));
        }
    });

    // Ajax request to check the status of the api
    $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/status/',
        type: 'GET',
        success: function (response) {
            if (response.status === 'OK') {
                $('#api_status').addClass('available');
            } else {
                $('#api_status').removeClass('available');
            }
        },
        error: function (error) {
            $('#api_status').removeClass('available');
        }
    });

    // Ajax request to retrieve places data
    $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/places_search/',
        type: 'POST',
        contentType: 'application/json',
        // Send an empty dictionary
        data: JSON.stringify({}),
        success: function(response) {
            // Loop through each place in the response
            response.forEach(function(place) {
                // Dynamically populate HTML elements for each place
                var html = '<article>' +
                    '<div class="headline">' +
                    '<div class="place_name">' +
                    '<h2>' + place.name + '</h2>' +
                    '</div>' +
                    '<div class="price_by_night">$' + place.price_by_night + '</div>' +
                    '</div>' +
                    '<div class="information">' +
                    '<div class="max_guest">' +
                    '<div class="guest_icon"></div>' +
                    '<p>' + place.max_guest + ' Guests</p>' +
                    '</div>' +
                    '<div class="number_rooms">' +
                    '<div class="bed_icon"></div>' +
                    '<p>' + place.number_rooms + ' Bedroom</p>' +
                    '</div>' +
                    '<div class="number_bathrooms">' +
                    '<div class="bath_icon"></div>' +
                    '<p>' + place.number_bathrooms + ' Bathroom</p>' +
                    '</div>' +
                    '</div>' +
                    '<div class="user"><b>Owner</b>: ' + place.user.first_name + '</div>' +
                    '<div class="description">' + place.description + '</div>' +
                    '</article>';
                // Append the elements to the DOM 
                $('.places').append(html);
            });
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
});
