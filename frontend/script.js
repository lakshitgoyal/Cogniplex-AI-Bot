document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const loadingIndicator = document.getElementById('loading-indicator');

    const docUploadBtn = document.getElementById('doc-upload-btn');
    const mediaAnalyzeBtn = document.getElementById('media-analyze-btn');

    const docUploadInput = document.getElementById('doc-upload');
    const mediaUploadInput = document.getElementById('media-upload');
    const mediaQueryInput = document.getElementById('media-query');


    const showLoading = (show) => {
        loadingIndicator.classList.toggle('hidden', !show);
    };

    const addMessage = (text, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = text;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    const handleSend = async () => {
        const query = chatInput.value.trim();
        if (!query) return;

        addMessage(query, 'user');
        chatInput.value = '';
        showLoading(true);

        const useRag = document.getElementById('rag-checkbox').checked;
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot');
        chatWindow.appendChild(botMessageElement);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, use_rag: useRag }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let botText = '';
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                botText += decoder.decode(value, { stream: true });
                botMessageElement.textContent = botText;
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }

        } catch (error) {
            botMessageElement.textContent = `Error: ${error.message}`;
        } finally {
            showLoading(false);
        }
    };

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });

    docUploadBtn.addEventListener('click', () => {
        docUploadInput.click();
    });

    docUploadInput.addEventListener('change', async () => {
        if (docUploadInput.files.length === 0) {
            return; 
        }
        const file = docUploadInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        showLoading(true);
        addMessage(`Uploading ${file.name}...`, 'bot');
        try {
            const response = await fetch('/api/upload/document', { method: 'POST', body: formData });
            const result = await response.json();
            if (!response.ok) throw new Error(result.detail);
            addMessage(`✅ Document processed: ${result.message}`, 'bot');
        } catch (error) {
            addMessage(`Error: ${error.message}`, 'bot');
        } finally {
            showLoading(false);
            docUploadInput.value = '';
        }
    });

    mediaAnalyzeBtn.addEventListener('click', () => {
        if (!mediaQueryInput.value.trim()) {
            alert('Please first type a question about the media.');
            return;
        }
        mediaUploadInput.click();
    });

    mediaUploadInput.addEventListener('change', async () => {
        if (mediaUploadInput.files.length === 0) {
            return;
        }
        const file = mediaUploadInput.files[0];
        const query = mediaQueryInput.value.trim();
        const formData = new FormData();
        formData.append('file', file);
        formData.append('query', query);
        
        showLoading(true);
        addMessage(`Analyzing ${file.name} with query: "${query}"`, 'user');
        try {
            const response = await fetch('/api/analyze/media', { method: 'POST', body: formData });
            const result = await response.json();
            if (!response.ok) throw new Error(result.detail);
            addMessage(result.analysis, 'bot');
        } catch (error) {
            addMessage(`Error: ${error.message}`, 'bot');
        } finally {
            showLoading(false);
            mediaUploadInput.value = '';
        }
    });
});