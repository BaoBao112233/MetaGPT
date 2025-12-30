// Configure marked.js options
marked.setOptions({
    highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            try {
                return hljs.highlight(code, { language: lang }).value;
            } catch (err) {}
        }
        return hljs.highlightAuto(code).value;
    },
    breaks: true,
    gfm: true
});

const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Add copy buttons to code blocks
function addCopyButtons() {
    document.querySelectorAll('pre code').forEach((block) => {
        // Skip if already has a copy button
        if (block.parentElement.parentElement.classList.contains('code-block-wrapper')) {
            return;
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        
        copyButton.onclick = async () => {
            try {
                await navigator.clipboard.writeText(block.textContent);
                copyButton.textContent = 'Copied!';
                copyButton.classList.add('copied');
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                    copyButton.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
                copyButton.textContent = 'Failed';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            }
        };
        
        // Wrap the pre element
        block.parentElement.parentNode.insertBefore(wrapper, block.parentElement);
        wrapper.appendChild(block.parentElement);
        wrapper.appendChild(copyButton);
    });
}

// Add a message to the chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const label = document.createElement('strong');
    label.textContent = isUser ? 'You:' : 'Assistant:';
    
    const markdownContent = document.createElement('div');
    markdownContent.className = 'markdown-content';
    
    if (isUser) {
        // For user messages, just display as text
        markdownContent.textContent = content;
    } else {
        // For assistant messages, render markdown
        markdownContent.innerHTML = marked.parse(content);
        // Highlight code blocks
        markdownContent.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
    
    messageContent.appendChild(label);
    messageContent.appendChild(markdownContent);
    messageDiv.appendChild(messageContent);
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Add copy buttons after rendering
    if (!isUser) {
        setTimeout(addCopyButtons, 100);
    }
    
    return markdownContent;
}

// Send a message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    messageInput.value = '';
    
    // Disable send button
    sendButton.disabled = true;
    const originalButtonText = sendButton.innerHTML;
    sendButton.innerHTML = '<span class="loading">Đang xử lý</span>';
    
    try {
        // Create assistant message placeholder
        const assistantContent = addMessage('');
        let fullResponse = '';
        
        // Use EventSource for streaming
        const response = await fetch('/chat/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, stream: true })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.slice(6);
                    if (data === '[DONE]') {
                        break;
                    }
                    fullResponse += data;
                    assistantContent.innerHTML = marked.parse(fullResponse);
                    // Highlight code blocks
                    assistantContent.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
        }
        
        // Add copy buttons to final response
        addCopyButtons();
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('❌ Đã xảy ra lỗi khi gửi tin nhắn. Vui lòng thử lại.');
    } finally {
        // Re-enable send button
        sendButton.disabled = false;
        sendButton.innerHTML = originalButtonText;
        messageInput.focus();
    }
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Focus on input on load
window.addEventListener('load', () => {
    messageInput.focus();
});
