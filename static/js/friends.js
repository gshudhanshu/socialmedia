// I wrote this code

// Add friend button click event
function add_friend(button) {
    const friend_id = button.getAttribute('data-friend-id')
    axios.post('/friends/add-friend', {
        friend_id: friend_id
    }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
        // On successfull response update the button text and disable it
        .then(function (response) {
            console.log(response);
            button.innerHTML = 'Sent'
            button.disabled = true
        })

        // On error response log the error and update the button text and disable it
        .catch(function (error) {
            console.log(error);
            if (error.response.data.request_sent_or_exist) {
                button.innerHTML = 'Already Exists'
                button.disabled = true
            } else if (error.response.data.request_sent_or_exist === false) {
                button.parentElement.parentElement.remove()
            }
        });
}

// Accept, Decline, Cancel, Remove friend button click event
function friend_request_accept_decline_cancel_remove(button) {
    const friend_id = button.getAttribute('data-friend-id')
    const data_request_type = button.getAttribute('data-request-type')
    const friend_link_id = button.getAttribute('data-friend-link-id')
    axios.put('/friends/accept-decline-cancel-remove', {
        friend_id: friend_id,
        friend_link_id: friend_link_id,
        request_type: data_request_type
    }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
        // On successful response update the button text and disable it
        .then(function (response) {
            console.log(response);
            if (data_request_type === 'accept') {
                button.innerHTML = 'Accepted'
                button.disabled = true
                button.nextElementSibling.remove()
            } else if (data_request_type === 'decline') {
                button.innerHTML = 'Declined'
                button.disabled = true
                button.previousElementSibling.remove()
            } else if (data_request_type === 'cancel') {
                button.innerHTML = 'Cancelled'
            } else if (data_request_type === 'remove') {
                button.innerHTML = 'Removed'
            }
            button.disabled = true
        })
        // On error log the error
        .catch(function (error) {
            console.log(error);
        })
}

// end of code I wrote