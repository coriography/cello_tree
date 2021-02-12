"use strict";

// event handler for add_cellist form in add_cellist.html
$('#add_cellist').on('submit', (evt) => {
    evt.preventDefault();

     //get form input
    const add_cellist_form_data = {
        'fname': $('#fname').val(),
        'lname': $('#lname').val(),
        'cello_details': $('#cello_details').val(),
        'bio': $('#bio').val(),
        'img_url': $('#img_url').val(),
        'music_url': $('#music_url').val(),
    }

    //send data to server.py
    $.post('/add_cellist', add_cellist_form_data, (res) => {
        //display response
        console.log(res)
        $('#response_here').text(res.fname, res.lname)
    });  

});

   
