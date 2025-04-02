document.addEventListener("DOMContentLoaded", function () {
    const chatBody = document.getElementById("chat-body");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    if (!chatBody || !userInput || !sendButton) {
        console.error("Missing elements! Check your HTML IDs.");
        return;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Append user message
        chatBody.innerHTML += `<p class="user-message"><b>You:</b> ${message}</p>`;
        userInput.value = "";
        chatBody.scrollTop = chatBody.scrollHeight;

        // Create bot message container (for streaming)
        const botMessageElement = document.createElement("p");
        botMessageElement.classList.add("bot-message");
        botMessageElement.innerHTML = "<b>Bot:</b> ";
        chatBody.appendChild(botMessageElement);

        // Fetch response from backend
        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            function readStream() {
                return reader.read().then(({ done, value }) => {
                    if (done) return;

                    const textChunk = decoder.decode(value, { stream: true });

                    // Check for website safety response
                    if (textChunk.includes("⚠️ Warning")) {
                        botMessageElement.innerHTML = `<b>Bot:</b> <span style="color: red; font-weight: bold;">${textChunk.replace(/\n/g, "<br>")}</span>`;
                    } else if (textChunk.includes("✅")) {
                        botMessageElement.innerHTML = `<b>Bot:</b> <span style="color: green; font-weight: bold;">${textChunk.replace(/\n/g, "<br>")}</span>`;
                    } else {
                        botMessageElement.innerHTML += textChunk.replace(/\n/g, "<br>");
                    }

                    chatBody.scrollTop = chatBody.scrollHeight;
                    return readStream();
                });
            }

            return readStream();
        })
        .catch(error => {
            botMessageElement.innerHTML += "<br><b style='color: red;'>⚠️ Error fetching response.</b>";
            console.error("Error:", error);
        });
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });
});
