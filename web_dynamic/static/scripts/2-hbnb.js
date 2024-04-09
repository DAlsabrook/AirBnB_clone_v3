$(document).ready(function () {
  $(document).on('change', "input[type='checkbox']", function () {
    const checkedList = [];
    // iterate through each checkbox
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
  $.ajax({
    // url: 'http://localhost:5001/api/v1/status/', //////////// For testing on windows
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
});
