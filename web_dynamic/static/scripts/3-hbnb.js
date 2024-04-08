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
          var articleTag = '<article>' +
            '<h2>' + place.name + '</h2>' +
            '</article>';
          $('.places').append(articleTag);
        });
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
