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
        $('#response_here').text(`${res.fname} ${res.lname} has been added to the database.`)
    });  

});


// event handler for login form on home.html
$('#login_form').on('submit', (evt) => {
    evt.preventDefault(); 

    const loginData = {
        'username_email': $('#username_email').val(),
        'password': $('#login_password').val()
    }

    $.post('/', loginData, (res) => {
        console.log(res);
    });

});

