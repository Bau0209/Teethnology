document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-messages');
    const welcomeHeader = document.getElementById('welcome-header');
    const chatBoxSection = document.getElementById('chat-box-section');
    const sendBtn = document.getElementById('send-btn');

    let started = false;

    // Reusable function to send message
    function sendMessage() {
        const message = input.value.trim();

        if (message !== '') {
            // First interaction: hide header, show chat container
            if (!started && welcomeHeader && chatBoxSection) {
                welcomeHeader.style.display = 'none';
                chatBoxSection.style.display = 'block';
                started = true;
            }

            // Append user's message
            const userMsg = document.createElement('div');
            userMsg.className = 'd-flex justify-content-end mb-2';
            userMsg.innerHTML = `<div class="bg-primary text-white p-2 rounded-3">${message}</div>`;
            chatBox.appendChild(userMsg);

            // Simulate bot response (you can replace this with actual AI logic later)
            const botMsg = document.createElement('div');
            botMsg.className = 'd-flex justify-content-start mb-2';
            botMsg.innerHTML = `<div class="bg-secondary text-white p-2 rounded-3">I'm looking that up for you...</div>`;
            chatBox.appendChild(botMsg);

            // Clear input
            input.value = '';

            // Scroll to bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Event: click send button
    sendBtn.addEventListener('click', sendMessage);

    // Event: press Enter key inside input field
    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent form submission or newline
            sendMessage();
        }
    });

});
