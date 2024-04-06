$(document).ready(function () {
    // new array to store the amenities that are checked
    const checkedAmenities = [];
    // checks if the checkbox is checked 
    $('input:checkbox').click(function () {
        // if it is, appends to the array Amenity
        if ($(this).is(":checked")) {
            checkedAmenities.push($(this).attr('data-name'));
        // if it isnt, remove the amenity
        } else {
            const amenityName = $(this).attr('data-name');
            const amenityIndex = checkedAmenities.indexOf(amenityName);
            // if the index equals -1, means the amenity was found and it is safe to remove
            if (amenityIndex !== -1) {
                checkedAmenities.splice(amenityIndex, 1);
            }
        }
        // updates the text of all h4 elements 
        $('.amenities h4').text(checkedAmenities.join(', '));
    });
});