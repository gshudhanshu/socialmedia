// I have taken the reference from
// https://testdriven.io/blog/django-channels/ tutorial
// modified the code to fit my needs

// Get the room name from the template
const roomName = JSON.parse(document.getElementById('roomName').textContent);
const chatLog = document.querySelector("#chatLog");
const chatMessageInput = document.querySelector("#chatMessageInput");
const chatMessageSend = document.querySelector("#chatMessageSend");
const onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// focus input field
chatMessageInput.focus();

// Listen for enter key press
chatMessageInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Listen for send button click
chatMessageSend.addEventListener('click', sendMessage);

let chatSocket = null;

// Connect to the WebSocket
function connect() {
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

    chatSocket.onopen = (e) => {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = (e) => {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(() => {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                appendMessage(`${data.user}: ${data.message}`);
                break;
            case "user_list":
                data.users.forEach(onlineUsersSelectorAdd);
                break;
            case "user_join":
                appendMessage(`${data.user} joined the room.`);
                onlineUsersSelectorAdd(data.user);
                break;
            case "user_leave":
                appendMessage(`${data.user} left the room.`);
                onlineUsersSelectorRemove(data.user);
                break;
            case "chat_history":
                data.messages.forEach((message) => appendMessage(`${message.user}: ${message.message}`));
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = (err) => {
        console.log(`WebSocket encountered an error: ${err.message}`);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}

// Send a message through the WebSocket
function sendMessage() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
}

// Add a user to the online users selector
function onlineUsersSelectorAdd(value) {
    if (!document.querySelector(`option[value='${value}']`)) {
        const newOption = document.createElement("option");
        newOption.value = value;
        newOption.innerHTML = value;
        onlineUsersSelector.appendChild(newOption);
    }
}

// Remove a user from the online users selector
function onlineUsersSelectorRemove(value) {
    const oldOption = document.querySelector(`option[value='${value}']`);
    if (oldOption !== null) oldOption.remove();
}

// Append a message to the chat log
function appendMessage(message) {
    chatLog.value += `${message}\n`;
}

connect();

// Add event listener to the online users selector
// When the user selects a user from the online users selector add the username to the chat input field
onlineUsersSelector.addEventListener('change', () => {
    chatMessageInput.value = `@${onlineUsersSelector.value} `;
    onlineUsersSelector.value = null;
    chatMessageInput.focus();
});
