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
    // localhost works and 0.0.0.0 does not. I have no idea why.
    // url: 'http://localhost:5001/api/v1/status/',
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

// You have to run the api in a seperate terminal.
// First set the environment variable "export HBNB_API_PORT = 5001"
  // and run the command "python3 -m api.v1.app"
// Second open a new terminal and set all env variable to run the flask app
  // "export HBNB_MYSQL_USER=hbnb_dev
  // export HBNB_MYSQL_PWD = hbnb_dev_pwd
  // export HBNB_MYSQL_HOST = localhost
  // export HBNB_MYSQL_DB = hbnb_dev_db
  // export HBNB_TYPE_STORAGE = db"
  // and run the command "python3 -m web_dynamic.0-hbnb"

// Idk if local host or 0.0.0.0 are the same thing but the 0's aint working.
// the task specifically tells us to use the 0.0.0.0 adress but when i do it
// just gives me an "invalid adress" error in the browser console.
// other than that task 3 is done
