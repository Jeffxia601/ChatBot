// Set partner name in header
// document.getElementById("partner-name").innerText = `Chat with ${partnerName}`;

// Send message to server
async function sendMessage() {
    const inputBox = document.getElementById("userInput");
    const message = inputBox.value.trim();
    if (!message) return;

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="user-msg">${message}</div>`;
    inputBox.value = "";
    inputBox.style.height = "auto";

    try {
        const response = await fetch("/chat/message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData.error || "AI is taking a nap, please try again later.");
            return;
        }

        const data = await response.json();
        chatbox.innerHTML += `<div class="bot-msg"><strong>${partnerName}:</strong> ${data.reply}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    } catch (err) {
        alert("Something went wrong. Please try again later.");
    }
}

// Handle Enter key as send trigger
document.getElementById("userInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

// Load chat history
window.onload = function () {
    fetch("/chat/history")
        .then(res => res.json())
        .then(data => {
            const chatbox = document.getElementById("chatbox");
            data.history.forEach(msg => {
                const sender = msg.role === 'user' ? 'You' : partnerName;
                const className = msg.role === 'user' ? 'user-msg' : 'bot-msg';
                chatbox.innerHTML += `<div class="${className}"><strong>${sender}:</strong> ${msg.content}</div>`;
            });
            chatbox.scrollTop = chatbox.scrollHeight;
        });
};

// Auto-expand textarea
document.getElementById("userInput").addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});
