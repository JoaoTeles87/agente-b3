document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const query = userInput.value.trim();
        if (query === '') return;

        appendMessage(query, 'user');
        userInput.value = '';

        fetch('http://127.0.0.1:8000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.response, 'agent');
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('Sorry, something went wrong.', 'agent');
        });
    }

    function appendMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        messageElement.appendChild(paragraph);

        if (sender === 'agent') {
            const refineButton = document.createElement('button');
            refineButton.textContent = 'Refine';
            refineButton.classList.add('refine-button');
            refineButton.addEventListener('click', () => {
                const refinedQuery = prompt('How would you like to refine the answer?', text);
                if (refinedQuery) {
                    sendMessage(refinedQuery);
                }
            });
            messageElement.appendChild(refineButton);
        }

        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
