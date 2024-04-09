$(document).ready(function () {
    console.log('Document loaded');

    // Listen for changes on amenity check boxes
    $(document).on('change', ".amenity input[type='checkbox']", function () {
        const amenityCheckedList = [];
        // Iterate through each checkbox
      $('.amenity input[type="checkbox"]').each(function () {
            // Add all checked names to the list
            if ($(this).is(':checked')) {
              amenityCheckedList.push($(this).attr('data-name'));
            }
        });
      if (amenityCheckedList.length === 0) {
            // If nothing is checked add the nbsp back
          $('.amenities .checkedList').html('&nbsp;');
        } else {
            // Update the h4 tag with the list of checked amenities
        $('.amenities .checkedList').text(amenityCheckedList.join(', '));
        }
    });

  // Listen for changes on state/city checkboxes
  $(document).on('change', ".locations input[type='checkbox']", function () {
    const stateCheckedList = [];
    // Iterate through each checkbox
    $('.state input[type="checkbox"], .city input[type="checkbox"]').each(function () {
      // Add all checked names to the list
      if ($(this).is(':checked')) {
        stateCheckedList.push($(this).attr('data-name'));
      }
    });
    if (stateCheckedList.length === 0) {
      // If nothing is checked add the nbsp back
      $('.locations .checkedList').html('&nbsp;');
    } else {
      // Update the h4 tag with the list of checked amenities
      $('.locations .checkedList').text(stateCheckedList.join(', '));
    }
  });

    // Ajax request to check the status of the api
    $.ajax({
        url: 'http://localhost:5001/api/v1/status/', ////////////for testing on windows
        // url: 'http://0.0.0.0:5001/api/v1/status/',
        type: 'GET',
        success: function (response) {
            if (response.status === 'OK') {
                console.log("API is available")
                $('#api_status').addClass('available');
            } else {
                console.log("API is not available")
                $('#api_status').removeClass('available');
            }
        },
        error: function (error) {
            $('#api_status').removeClass('available');
        }
    });


  function getPlaces(data = {}) {
    console.log("Data sent to api: ", data)
    // Ajax request to retrieve places data
    $.ajax({
      url: 'http://localhost:5001/api/v1/places_search/', /////////////for testing on windows
      // url: 'http://0.0.0.0:5001/api/v1/places_search/',
      type: 'POST',
      contentType: 'application/json',
      // Send an empty dictionary
      data: JSON.stringify({data}),
      success: function(response) {
        // Loop through each place in the response
        response.forEach(function(place) {
          console.log(" places")
          // Ajax request to get the user object from the user_id in place
          $.ajax({
              url: 'http://localhost:5001/api/v1/users/' + place.user_id, //////////////for testing on windows
              // url: 'http://0.0.0.0:5001/api/v1/users/' + place.user_id,
              type: 'GET',
              success: function(user) {
                  place.user = user.first_name + ' ' + user.last_name;
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
              },
              error: function(xhr, status, error) {
                  console.error('Error from user ajax:', error);
              },
          });
        });
      },
      error: function(xhr, status, error) {
          console.error('Error from places search ajax:', error);
      }
    });
  }

  getPlaces();

  // Call getPlaces with the checked boxes when the filter button is clicked
  $('.filters button').on('click', function () {
    // Get the list of checked amenities
    const data = {};
    const amenities = [];
    const states = [];
    const cities = [];
    $('.amenity > input[type="checkbox"]').each(function () {
      if ($(this).is(':checked')) {
        amenities.push($(this).attr('data-id'));
      }
    });
    $('.state > input[type="checkbox"]').each(function () {
      if ($(this).is(':checked')) {
        states.push($(this).attr('data-id'));
      }
    });
    $('.city > input[type="checkbox"]').each(function () {
      if ($(this).is(':checked')) {
        cities.push($(this).attr('data-id'));
      }
    });
    if (amenities.length > 0) {
      data['amenities'] = amenities;
    }
    if (states.length > 0) {
      data['states'] = states;
    }
    if (cities.length > 0) {
      data['cities'] = cities;
    }
    // Clear the places div
    $('.places').empty();
    getPlaces(data);
  });
});
