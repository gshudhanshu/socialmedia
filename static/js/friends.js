function add_friend(button) {
    const friend_id = button.getAttribute('data-friend-id')
    axios.post('/api/friends/add-friend', {
        friend_id: friend_id
    }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
        .then(function (response) {
            console.log(response);
            button.innerHTML = 'Sent'
            button.disabled = true
        })
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

function friend_request_accept_decline_cancel_remove(button) {
    const friend_id = button.getAttribute('data-friend-id')
    const data_request_type = button.getAttribute('data-request-type')
    axios.put('/api/friends/accept-decline-cancel', {
        friend_id: friend_id,
        request_type: data_request_type
    }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
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
        .catch(function (error) {
            console.log(error);
        })
}
