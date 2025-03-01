document.addEventListener("DOMContentLoaded", function () {
    const chatBody = document.getElementById("chat-body");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    // Check if elements exist
    if (!chatBody || !userInput || !sendButton) {
        console.error("Missing elements! Check your HTML IDs.");
        return;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Append user message
        chatBody.innerHTML += `<p class="user-message">You: ${message}</p>`;
        userInput.value = "";

        // Send message to Flask backend
        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            chatBody.innerHTML += `<div class="message bot-message"><b>Bot:</b> ${data.response.replace(/\n/g, '<br>')}</div>`;

            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => console.error("Error:", error));
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });
});
