// chat.js

// Function to add a message to the chat window
function addMessage(message) {
    const chatWindow = document.querySelector('.chat-window');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.textContent = message;
    chatWindow.appendChild(messageDiv);

    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Function to update the user list
function updateUserList(users) {
    const userList = document.querySelector('.user-list ul');
    userList.innerHTML = ''; // Clear the user list

    users.forEach(user => {
        const listItem = document.createElement('li');
        listItem.textContent = user;
        userList.appendChild(listItem);
    });
}

// Send a message when the "Send" button is clicked
const sendButton = document.getElementById('send-button');
sendButton.addEventListener('click', function() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value;
    if (message) {
        // You can send the message to a server or handle it as needed
        addMessage(`User: ${message}`);
        chatInput.value = ''; // Clear the input field
    }
});

// Example: Update the user list
const users = ['User 1', 'User 2', 'User 3']; // Replace with actual user data
updateUserList(users);
