"use strict";


async function imageUpload(files) {
    const url = "https://api.cloudinary.com/v1_1/cellotree/image/upload";
    const uploadData = new FormData(); 

    let file = files[0];
    uploadData.append("file", file);
    uploadData.append("upload_preset", "fb2hjysk");

    let response = await fetch(url, {
        method: "POST",
        body: uploadData
    });

    let json = await response.json();

    return json.url
}

// event handler for add_cellist form in add_cellist.html
$('#add_cellist').on('submit', (evt) => {
    evt.preventDefault();

    const media_files = $('#photo_upload').prop('files');
    const cloud_url = imageUpload(media_files);

    cloud_url.then((res_url) => {
        //get form input
        const add_cellist_form_data = {
            'fname': $('#fname').val(),
            'lname': $('#lname').val(),
            'cello_details': $('#cello_details').val(),
            'bio': $('#bio').val(),
            'img_url': res_url,
            'music_url': $('#music_url').val(),
        }

        // send data to server.py
        $.post('/add_cellist', add_cellist_form_data, (res) => {
            if (res.status === 'ok') {
                // hide add_cellist form, display response message,
                // display add_another button, reset form fields
                $('#add_cellist').addClass("d-none");
                $('#add_response').html(`<a href="/cellist_profile/${res.cellist_id}">${res.fname} ${res.lname}</a> has been added to the database.`);
                $('#add_another_btn').removeClass("d-none");
                $('#add_cellist').trigger('reset');
            } else if (res.status === 'error') {
                // hide add_cellist form, display response message,
                // display add_another button, reset form fields
                $('#add_cellist').addClass("d-none");
                $('#add_response').html(`<a href="/cellist_profile/${res.cellist_id}">${res.fname} ${res.lname}</a> already exists in the database.`);
                $('#add_another_btn').removeClass("d-none");
                $('#add_cellist').trigger('reset');
            };
        });  
    });
});


// event handler for add another cellist button
$('#add_another_btn').on('click', function() {
    $('#add_cellist').removeClass("d-none");
    $('#add_response').html('');
    $('#add_another_btn').addClass("d-none");
});

// event handler for update_cellist form in add_cellist.html
$('#update_cellist').on('submit', (evt) => {
    evt.preventDefault();

    const media_files = $('#update_photo').prop('files');
    const cloud_url = imageUpload(media_files);

    cloud_url.then((res_url) => {
        //get form input
        const update_cellist_form_data = {
            'cellist_id': $('#update_cellist_id').val(),
            'fname': $('#update_fname').val(),
            'lname': $('#update_lname').val(),
            'cello_details': $('#update_cello_details').val(),
            'bio': $('#update_bio').val(),
            'img_url': res_url,
            'music_url': $('#update_music_url').val(),
        }

        //send data to server.py
        $.post('/api/update_cellist', update_cellist_form_data, (res) => {
            if (res.status === 'ok') {
                location.href = `/cellist_profile/${update_cellist_form_data.cellist_id}`;
            }
        });
    })
});


// event handler for login form on home.html
$('#login_form').on('submit', (evt) => {
    evt.preventDefault(); 

    const loginData = {
        'username_email': $('#username_email').val(),
        'login_password': $('#login_password').val()
    }

    $.post('/api/login', loginData, (res) => {
        if (res.status === 'ok') {
            $('#display_response').text(`${res.username_email} is logged in`);
            $('#nav_login_logout').text(`Log out ${res.username} | `);
        } else if (res.status === 'error') {
            $('#display_response').text(res.msg);
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
        if (res.status === 'teacher_eq_student') {
            $('#add_link_response').text('Cannot add link between a teacher and themselves.')
        } else if (res.status === 'link_exists') {
            $('#add_link_response').text('That link already exists.')
        } else if (res.status === 'ok') {
            // $('#add_link_response').text(`${res.teacher_id} added as teacher.`)
            $('#teachers_list').prepend(`
                <li>
                    <a href="/cellist_profile/${res.teacher_id}">
                        ${res.teacher_fname} ${res.teacher_lname}
                    </a>
                </li>
            `)
        }
    });

});

// event handler for add_post form on cellist_profile.html
$('#add_post').on('submit', (evt) => {
    evt.preventDefault(); 

    const postData = {
        'post_content': $('#post_content').val(),
        'cellist_id_from_profile': $('#cellist_id_from_profile').val()
    }

    $.post('/api/add_post', postData, (res) => {
        if (res.status === 'ok') {
            $('#add_post').html(`
                <div class="my-4">
                    <h5>${res.new_username}</h5>
                    <h6>${res.new_date} UTC</h6>
                    <p>${res.new_content}</p>
                    <p>
                        <i id="upvote_icon_${res.new_post_id}" class="fas fa-arrow-alt-circle-up"></i>
                        <span id="upvotes_count_${res.new_post_id}" class="">
                            ${res.new_post_upvotes|length} upvotes
                        </span>
                    </p>
                    <button id="toggle_upvote_${res.new_post_id}" class="btn btn-secondary"
                        onclick="toggleUpvote('${res.new_post_id}')">
                        Upvote
                    </button>
                </div>
            `);
        }
    });

});

// use button with onClick function and pass in post id
// function defines post id as object and executes ajax call
function toggleUpvote(post_id) {
    const upvoteData = {
        'post_id': post_id
    }

    $.post('/api/upvote_post', upvoteData, (res) => {
        console.log(res);
        $(`#upvotes_count_${post_id}`).text(`Upvotes: ${res.upvotes_count}`);
        $(`#toggle_upvote_${post_id}`).text(res.msg);
    });
};

