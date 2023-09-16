function saveStatus(button) {
//     get element by id "status-input" then get the value of the input
    const status_input = document.getElementById("status-input")
    const status_message = document.getElementById("status-message")
    const modal = document.getElementById("hs-focus-management-modal")
    const closeButton = document.getElementById("status-message-close-button");


    axios.put('/profile/status', {
        status_message: status_input.value
    }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token

        }
    })
        .then(function (response) {
            console.log(response);
            status_message.innerHTML = response.data.status_message
            closeButton.click();

        })
        .catch((error) => {
            console.log(error)
        })

}