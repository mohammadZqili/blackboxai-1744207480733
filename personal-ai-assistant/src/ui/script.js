document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const historyList = document.getElementById('history-list');
    const messageTemplate = document.getElementById('message-template');

    // Load chat history on page load
    loadHistory();

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('You', message);
        userInput.value = '';

        try {
            // Send message to backend
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input: message }),
            });

            const data = await response.json();

            if (response.ok) {
                // Add AI response to chat
                addMessage('AI Assistant', data.response);
                
                // Update history
                loadHistory();
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('System', 'Sorry, there was an error processing your request.');
        }
    });

    // Function to add a message to the chat
    function addMessage(sender, text) {
        const messageDiv = messageTemplate.content.cloneNode(true);
        const messageContainer = messageDiv.querySelector('.message');
        const icon = messageDiv.querySelector('.fas');
        const nameDiv = messageDiv.querySelector('.font-medium');
        const textDiv = messageDiv.querySelector('.mt-1');

        // Set appropriate icon and styling based on sender
        if (sender === 'AI Assistant') {
            icon.classList.remove('fa-user');
            icon.classList.add('fa-robot');
            messageContainer.classList.add('bg-blue-50');
        } else if (sender === 'System') {
            icon.classList.remove('fa-user');
            icon.classList.add('fa-exclamation-circle');
            messageContainer.classList.add('bg-red-50');
        }

        nameDiv.textContent = sender;
        textDiv.textContent = text;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to load chat history
    async function loadHistory() {
        try {
            const response = await fetch('/history');
            const data = await response.json();

            if (response.ok) {
                historyList.innerHTML = '';
                data.history.reverse().forEach(interaction => {
                    const historyItem = document.createElement('div');
                    historyItem.className = 'p-4 border rounded-lg hover:bg-gray-50 transition-colors';
                    historyItem.innerHTML = `
                        <div class="flex justify-between items-start mb-2">
                            <div class="font-medium text-gray-800">Q: ${interaction.text.split('\nResponse:')[0].replace('Query: ', '')}</div>
                            <div class="text-sm text-gray-500">${new Date(interaction.timestamp).toLocaleString()}</div>
                        </div>
                        <div class="text-gray-600">A: ${interaction.text.split('\nResponse:')[1]}</div>
                    `;
                    historyList.appendChild(historyItem);
                });
            } else {
                throw new Error(data.error || 'Failed to load history');
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }
});
