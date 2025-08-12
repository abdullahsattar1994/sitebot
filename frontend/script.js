// Get DOM elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');

// File upload functionality
uploadZone.addEventListener('click', () => {
    fileInput.click();
});

// Handle file selection
fileInput.addEventListener('change', handleFiles);

// Drag and drop functionality
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'rgba(255, 255, 255, 0.8)';
});

uploadZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'rgba(255, 255, 255, 0.3)';
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    const files = e.dataTransfer.files;
    handleFiles({ target: { files } });
});

// Handle file uploads
async function handleFiles(event) {
    const files = event.target.files;
    if (files.length === 0) return;

    // Show uploading state
    uploadZone.innerHTML = `
        <div class="upload-content">
            <i class="fas fa-spinner fa-spin upload-icon"></i>
            <h3>Uploading ${files.length} file(s)...</h3>
            <p>Processing your documents</p>
        </div>
    `;

    const formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        // Show success state
        uploadZone.innerHTML = `
            <div class="upload-content">
                <i class="fas fa-check-circle upload-icon" style="color: #4CAF50;"></i>
                <h3>Upload Complete!</h3>
                <p>${result.message}</p>
            </div>
        `;

        // Clear welcome message and enable chat
        document.querySelector('.welcome-message').innerHTML = `
            <i class="fas fa-robot"></i>
            <p>Your documents are ready! Ask me anything about them.</p>
        `;

    } catch (error) {
        // Show error state
        uploadZone.innerHTML = `
            <div class="upload-content">
                <i class="fas fa-exclamation-triangle upload-icon" style="color: #f44336;"></i>
                <h3>Upload Failed</h3>
                <p>Please try again</p>
            </div>
        `;
    }
}

// Chat functionality
sendButton.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    chatInput.value = '';

    // Show thinking state
    const thinkingId = addMessage('Thinking...', 'ai', true);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const result = await response.json();

        // Remove thinking message and add real response
        document.getElementById(thinkingId).remove();
        addMessage(result.response, 'ai');

    } catch (error) {
        document.getElementById(thinkingId).remove();
        addMessage('Sorry, something went wrong. Please try again.', 'ai');
    }
}

function addMessage(text, sender, isThinking = false) {
    const messageId = 'msg-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.id = messageId;
    messageDiv.textContent = text;

    if (isThinking) {
        messageDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Thinking...';
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageId;
}