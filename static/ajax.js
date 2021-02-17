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
        if (res.status === 'ok') {
            $('#response_here').text(`${res.fname} ${res.lname} has been added to the database.`)
        } else if (res.status === 'error') {
            $('#response_here').text(`${res.fname} ${res.lname} already exists in the database.`)
        }
    });  

});


// event handler for login form on home.html
$('#login_form').on('submit', (evt) => {
    evt.preventDefault(); 

    const loginData = {
        'username_email': $('#username_email').val(),
        'login_password': $('#login_password').val()
    }

    $.post('/api/login', loginData, (res) => {
        console.log(res);
        if (res.status === 'ok') {
            $('#display_response').text(`${res.username_email} is logged in`)
        } else if (res.status === 'error') {
            $('#display_response').text(res.msg)
        }
    });
});

// event handler for create_account form on home.html
$('#create_account').on('submit', (evt) => {
    evt.preventDefault(); 

    const loginData = {
        'username': $('#username').val(),
        'email': $('#email').val(),
        'create_password': $('#create_password').val()
    }

    $.post('/api/create_account', loginData, (res) => {
        console.log(res);
        if (res.status === 'username_error') {
            $('#display_response').text(`${res.username} already exists`)
        } else if (res.status === 'email_error') {
            $('#display_response').text(`${res.email} already exists`)
        } else if (res.status === 'ok') {
            $('#display_response').text(`account created for ${res.username}`)
        }
    });

});

// event handler for add_link form on cellist_profile.html
$('#add_link').on('submit', (evt) => {
    evt.preventDefault(); 

    const linkData = {
        'teacher_id': $('#teacher_id').val(),
        'student_id': $('#student_id').val()
    }

    $.post('/api/create_link', linkData, (res) => {
        console.log(res);
        if (res.status === 'teacher_eq_student') {
            $('#add_link_response').text('Cannot add link between a teacher and themselves.')
        } else if (res.status === 'link_exists') {
            $('#add_link_response').text('That link already exists.')
        } else if (res.status === 'ok') {
            $('#add_link_response').text(`${res.teacher_id} added as teacher.`)

            // TODO: add ajax to populate into teacher list??

        }
    });

});