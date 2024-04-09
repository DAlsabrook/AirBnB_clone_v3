$(document).ready(function () {
    console.log("Document ready")
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
        url: 'http://localhost:5001/api/v1/status/', //for testing on windows
        // url: 'http://0.0.0.0:5001/api/v1/status/',
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
        url: 'http://localhost:5001/api/v1/places_search/', //for testing on windows
        // url: 'http://0.0.0.0:5001/api/v1/places_search/',
        type: 'POST',
        contentType: 'application/json',
        // Send an empty dictionary
        data: JSON.stringify({
            "states":
                ["9799648d-88dc-4e63-b858-32e6531bec5c", "5976f0e7-5c5f-4949-aae0-90d68fd239c0"] // California, florida
            // "cities":
            //     ["05b0b99c-f10e-4e3a-88d1-b3187d6998ee"] // San francisco
            // "amenities":
            //     ["2f055228-5fd3-4b1d-a021-7e4b9b7d70a6", // tv
            //     "43de9883-8b2d-44dc-81d3-8b719ea50734", // Heating
            //     "47327246-6852-4c70-b3db-77077ab61a32", // Kid friendly
            //     "6b9c3987-a344-4baf-8d11-077d719688ba", // Lock on bedroom door
            //     "c4b9d932-71f4-4f10-9e09-502c3eb67ee2",] // safety card
        }),
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
                    '<div class="user"><b>Owner</b>: ' + place.user + '</div>' +
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
