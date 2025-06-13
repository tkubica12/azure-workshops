<script>
  import { onMount, afterUpdate } from 'svelte';
  
  // Hardcoded users for development
  const USERS = [
    { userId: "user_001", name: "Alice Johnson", email: "alice@example.com" },
    { userId: "user_002", name: "Bob Smith", email: "bob@example.com" },
    { userId: "user_003", name: "Carol White", email: "carol@example.com" }
  ];
  let question = '';
  let messages = [];
  let sessionId;
  let messagesContainer;  let selectedUser = USERS[0]; // Default to first user
  let showUserDropdown = false;
  let showHistory = false;
  let showMemory = false;
  let userMemory = null;
  let conversations = [];
  let editingTitleSessionId = null;
  let editingTitle = '';
  const API_URL = import.meta.env.API_URL || window._env_?.API_URL;
  const SSE_URL = import.meta.env.SSE_URL || window._env_?.SSE_URL;
  const HISTORY_API_URL = import.meta.env.HISTORY_API_URL || window._env_?.HISTORY_API_URL;
  const MEMORY_API_URL = import.meta.env.MEMORY_API_URL || window._env_?.MEMORY_API_URL;

  onMount(async () => {
    try {
      const response = await fetch(`${API_URL}/api/session/start`, { 
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: selectedUser.userId })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      sessionId = data.sessionId;
      localStorage.setItem('session_id', sessionId);
      console.log('Session started with ID:', sessionId, 'for user:', selectedUser.name);
      
      // Load conversation history for the user
      await loadConversationHistory();
    } catch (error) {
      console.error('Failed to start session:', error);
      sessionId = localStorage.getItem('session_id') || crypto.randomUUID();
      localStorage.setItem('session_id', sessionId);
    }
  });

  afterUpdate(() => {
    // Auto-scroll to bottom on new messages
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }  });
  async function switchUser(user) {
    selectedUser = user;
    // Clear current session and messages
    sessionId = null;
    messages = [];
    localStorage.removeItem('session_id');
    
    // Start new session for the selected user
    try {
      const response = await fetch(`${API_URL}/api/session/start`, { 
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: selectedUser.userId })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      sessionId = data.sessionId;
      localStorage.setItem('session_id', sessionId);
      console.log('Session started with ID:', sessionId, 'for user:', selectedUser.name);
      
      // Load conversation history for the new user
      await loadConversationHistory();
    } catch (error) {
      console.error('Failed to start session:', error);
      sessionId = crypto.randomUUID();
      localStorage.setItem('session_id', sessionId);
    }
  }

  async function loadConversationHistory() {
    try {
      const response = await fetch(`${HISTORY_API_URL}/conversations/${selectedUser.userId}`);
      if (response.ok) {
        conversations = await response.json();
        console.log('Loaded conversation history:', conversations);
      } else {
        console.error('Failed to load conversation history:', response.status);
        conversations = [];
      }
    } catch (error) {
      console.error('Error loading conversation history:', error);
      conversations = [];
    }
  }
  async function loadConversation(conversationSessionId) {
    try {
      const response = await fetch(`${HISTORY_API_URL}/conversations/${selectedUser.userId}/${conversationSessionId}/messages`);
      if (response.ok) {
        const conversationData = await response.json();        messages = conversationData.messages.map(msg => ({
          id: msg.messageId,
          sender: msg.role,
          content: msg.content,
          timestamp: msg.timestamp
        }));
        // Switch to this conversation
        sessionId = conversationSessionId;
        localStorage.setItem('session_id', conversationSessionId);
        showHistory = false;
        console.log('Loaded conversation:', conversationSessionId);
      } else {
        console.error('Failed to load conversation:', response.status);
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  }
  async function updateConversationTitle(sessionId, newTitle) {
    try {
      const response = await fetch(`${HISTORY_API_URL}/conversations/${selectedUser.userId}/${sessionId}/title`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTitle })
      });
      
      if (response.ok) {
        // Update the local conversations list
        conversations = conversations.map(conv => 
          conv.sessionId === sessionId ? { ...conv, title: newTitle } : conv
        );
        editingTitleSessionId = null;
        editingTitle = '';
        console.log('Updated conversation title:', newTitle);
        
        // Refresh conversation history to ensure consistency
        await loadConversationHistory();
      } else {
        console.error('Failed to update conversation title:', response.status);
      }
    } catch (error) {
      console.error('Error updating conversation title:', error);
    }
  }

  function startEditingTitle(sessionId, currentTitle) {
    editingTitleSessionId = sessionId;
    editingTitle = currentTitle || '';
  }

  function cancelEditingTitle() {
    editingTitleSessionId = null;
    editingTitle = '';
  }

  function saveTitle(sessionId) {
    if (editingTitle.trim()) {
      updateConversationTitle(sessionId, editingTitle.trim());
    } else {
      cancelEditingTitle();
    }
  }

  async function send() {
    if (!question.trim() || !sessionId) return;
    const chatMessageId = crypto.randomUUID();
    const userMessage = { sender: 'user', content: question, id: chatMessageId };
    messages = [...messages, userMessage];

    // Prepare placeholder for assistant response
    const assistantMessagePlaceholder = { sender: 'assistant', content: '...', id: crypto.randomUUID(), isLoading: true };
    messages = [...messages, assistantMessagePlaceholder];

    const currentQuestion = question;
    question = ''; // Clear input

    try {
      // 1. Post message to front service
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: currentQuestion, sessionId, chatMessageId, userId: selectedUser.userId }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const chatResponse = await response.json();
      console.log('Message queued:', chatResponse);

      // 2. Connect to SSE service for streaming response
      const sseResponse = await fetch(`${SSE_URL}/api/stream/${sessionId}/${chatMessageId}`);
      
      if (!sseResponse.ok) {
        throw new Error(`SSE connection failed! status: ${sseResponse.status}`);
      }

      // Handle SSE stream
      const reader = sseResponse.body.getReader();
      const decoder = new TextDecoder();
      let assistantResponse = '';

      messages = messages.map(msg => 
        msg.id === assistantMessagePlaceholder.id ? { ...msg, isLoading: true, content: '' } : msg
      );

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.substring(6);            if (dataStr === '__END__') {
              messages = messages.map(msg => 
                msg.id === assistantMessagePlaceholder.id ? { ...msg, isLoading: false } : msg
              );
              
              // Refresh conversation history after message completion
              // This ensures new conversations appear in the history immediately
              await loadConversationHistory();
              
              return; // End of stream
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.token) {
                assistantResponse += data.token;
                messages = messages.map(msg => 
                  msg.id === assistantMessagePlaceholder.id ? { ...msg, content: assistantResponse, isLoading: true } : msg
                );
              }
              if (data.error) {
                messages = messages.map(msg => 
                  msg.id === assistantMessagePlaceholder.id ? { ...msg, content: data.error, isLoading: false, isError: true } : msg
                );
                return;
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e, 'Raw data:', dataStr);
            }
          }
        }
      }
    } catch (error) {
      console.error('Failed to send message or process stream:', error);
      messages = messages.map(msg => 
        msg.id === assistantMessagePlaceholder.id ? { ...msg, content: 'Error: Could not connect to the server.', isLoading: false, isError: true } : msg
      );
    }  }
  async function toggleHistory() {
    // If opening the history panel, refresh the conversation list
    if (!showHistory) {
      await loadConversationHistory();
    }
    showHistory = !showHistory;
  }
  async function startNewChat() {
    try {
      // Clear current session and messages
      sessionId = null;
      messages = [];
      localStorage.removeItem('session_id');
      
      // Start new session for the current user
      const response = await fetch(`${API_URL}/api/session/start`, { 
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: selectedUser.userId })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      sessionId = data.sessionId;
      localStorage.setItem('session_id', sessionId);
      console.log('New session started with ID:', sessionId, 'for user:', selectedUser.name);
      
      // Close history panel if open
      showHistory = false;
      
      // Refresh conversation history to show the new session
      await loadConversationHistory();
    } catch (error) {
      console.error('Failed to start new session:', error);
      sessionId = crypto.randomUUID();
      localStorage.setItem('session_id', sessionId);
    }
  }

  async function loadUserMemory() {
    try {
      const response = await fetch(`${MEMORY_API_URL}/api/memory/users/${selectedUser.userId}/memories`);
      if (response.ok) {
        userMemory = await response.json();
        console.log('Loaded user memory:', userMemory);
      } else {
        console.error('Failed to load user memory:', response.status);
        userMemory = null;
      }
    } catch (error) {
      console.error('Error loading user memory:', error);
      userMemory = null;
    }
  }

  async function deleteUserMemory() {
    if (!confirm('Are you sure you want to delete all your memories? This action cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`${MEMORY_API_URL}/api/memory/users/${selectedUser.userId}/memories`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        console.log('User memory deleted successfully');
        userMemory = null;
        // Show success message or notification
        alert('Your memories have been deleted successfully.');
      } else if (response.status === 404) {
        console.log('No user memories found to delete');
        userMemory = null;
        alert('No memories found to delete.');
      } else {
        console.error('Failed to delete user memory:', response.status);
        alert('Failed to delete memories. Please try again.');
      }
    } catch (error) {
      console.error('Error deleting user memory:', error);
      alert('Error deleting memories. Please check your connection and try again.');
    }
  }

  async function toggleMemory() {
    // If opening the memory panel, refresh the user memory
    if (!showMemory) {
      await loadUserMemory();
    }
    showMemory = !showMemory;
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    .chat-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 600px;
    min-height: 60vh;
    max-height: 80vh;
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin: 0 auto;
    padding: 2rem 0 1rem 0;
    overflow: hidden;
    transition: all 0.3s ease;
  }.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    font-size: 1.3rem;
    font-weight: 500;
    color: #222;
    margin-bottom: 1.5rem;
    letter-spacing: 0.01em;
  }
  .header-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .control-button {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 0.6rem;
    cursor: pointer;
    font-size: 0;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    color: #555;
  }
  
  .control-button:hover {
    background: #e9ecef;
    transform: translateY(-1px);
    color: #333;
  }
  
  .control-button.active {
    background: #e9ecef;
    border-color: #333;
    color: #333;
  }
  
  .control-button.active .control-icon {
    transform: scale(1.1);
  }
  
  .control-icon {
    width: 18px;
    height: 18px;
    fill: currentColor;
    transition: all 0.2s ease;
  }
    /* User selector styles */
  .user-selector {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .user-dropdown {
    position: relative;
  }  .user-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.2s;
    color: inherit;
    font-family: inherit;
  }  .user-button:hover {
    background: #e9ecef;
  }
  .user-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    z-index: 10;
    min-width: 200px;
  }
  .user-menu-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    border-bottom: 1px solid #f1f3f4;
    transition: background 0.2s;
  }
  .user-menu-item:hover {
    background: #f8f9fa;
  }
  .user-menu-item:last-child {
    border-bottom: none;
  }  .user-menu-item.selected {
    background: #e9ecef;
    color: #333;
  }
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 0 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }
  .message {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    max-width: 80%;
    font-size: 1.08rem;
    line-height: 1.6;
    word-break: break-word;
  }
  .message.user {
    align-self: flex-end;
    justify-content: flex-end;
    background: #f5f6f8;
    color: #222;
    border-radius: 16px 16px 4px 16px;
    padding: 0.7rem 1.2rem;
    margin-right: 0.2rem;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03);
  }
  .message.assistant {
    align-self: flex-start;
    justify-content: flex-start;
    background: #f9f9fa;
    color: #222;
    border-radius: 16px 16px 16px 4px;
    padding: 0.7rem 1.2rem;
    margin-left: 0.2rem;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03);
  }
  .message.assistant .content {
    white-space: pre-wrap; /* Allow wrapping of long tokens */
  }
  .message.assistant.isLoading .content::after {
    content: '▋'; /* Blinking cursor */
    animation: blink 1s step-start infinite;
  }
  @keyframes blink {
    50% { opacity: 0; }
  }
  .message.isError .content {
    color: red;
  }
  .content {
    flex: 1;
  }
  .chat-input {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1.2rem 2rem 0.5rem 2rem;
    background: #fff;
    border-top: 1px solid #f0f0f0;
    position: sticky;
    bottom: 0;
    z-index: 2;
  }
  input {
    flex: 1;
    padding: 0.9rem 1.2rem;
    font-size: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 999px;
    background: #fafbfc;
    outline: none;
    transition: border 0.2s;
  }  input:focus {
    border: 1.5px solid #888;
    background: #fff;
  }
  button {
    padding: 0.7rem 1.5rem;
    background-color: #222;
    color: white;
    border: none;
    border-radius: 999px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
  }
  button:hover {
    background: #444;
  }
    /* Memory Panel Styles */
  .memory-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 420px;
    max-height: 85vh;
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.12);
    z-index: 1000;
    overflow: hidden;
    font-family: 'Roboto', sans-serif;
    border: 1px solid #e0e0e0;
  }
  
  .memory-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    cursor: pointer;
  }
  
  .memory-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid #f0f0f0;
    background: #fafbfc;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .memory-header h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 500;
    color: #222;
    font-family: 'Roboto', sans-serif;
  }
  
  .close-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    background: none;
    border: none;
    border-radius: 50%;
    color: #666;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0;
  }
  
  .close-button:hover {
    background: #e9ecef;
    color: #333;
    transform: scale(1.1);
  }
  
  .memory-header-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
    .delete-memory-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    background: none;
    border: none;
    border-radius: 50%;
    color: #666;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0;
  }
  
  .delete-memory-button:hover {
    background: #e9ecef;
    color: #333;
    transform: scale(1.1);
  }
  
  .memory-content {
    padding: 0;
    max-height: 70vh;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #c0c0c0 transparent;
  }
  
  .memory-content::-webkit-scrollbar {
    width: 6px;
  }
  
  .memory-content::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .memory-content::-webkit-scrollbar-thumb {
    background-color: #c0c0c0;
    border-radius: 3px;
  }
  
  .memory-content::-webkit-scrollbar-thumb:hover {
    background-color: #a0a0a0;
  }
  
  .memory-section {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid #f5f5f5;
  }
  
  .memory-section:last-child {
    border-bottom: none;
  }
  
  .memory-section h4 {
    margin: 0 0 1rem 0;
    font-size: 1rem;
    font-weight: 500;
    color: #222;
    font-family: 'Roboto', sans-serif;
    display: flex;
    align-items: center;
  }
    .memory-section h4::before {
    content: '';
    width: 4px;
    height: 1rem;
    background: #666;
    border-radius: 2px;
    margin-right: 0.75rem;
  }
  
  .memory-section h5 {
    margin: 1rem 0 0.5rem 0;
    font-size: 0.9rem;
    font-weight: 500;
    color: #555;
    font-family: 'Roboto', sans-serif;
  }
  
  .memory-section ul {
    margin: 0;
    padding-left: 0;
    list-style: none;
  }
  
  .memory-section li {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #555;
    font-family: 'Roboto', sans-serif;
    padding: 0.5rem 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 3px solid #e9ecef;
  }
  
  .subsection {
    margin-top: 1rem;
  }
  
  .subsection:first-child {
    margin-top: 0;
  }
  
  .no-data {
    font-size: 0.85rem;
    color: #999;
    font-style: italic;
    margin: 0;
    padding: 1rem;
    text-align: center;
    background: #f8f9fa;
    border-radius: 8px;
    font-family: 'Roboto', sans-serif;
  }
  
  .no-memory {
    text-align: center;
    color: #666;
    padding: 3rem 2rem;
    font-family: 'Roboto', sans-serif;
  }
  
  .no-memory p {
    margin: 0.5rem 0;
    font-size: 0.9rem;
    line-height: 1.5;
  }
  
  .no-memory p:first-child {
    font-size: 1rem;
    font-weight: 500;
    color: #555;
  }
  
  /* History Panel Styles */
  .chat-layout {
    display: flex;
    position: relative;
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
    min-height: 60vh;
    max-height: 80vh;
  }
  
  .history-panel {
    width: 320px;
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
    margin-right: 1rem;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    font-family: 'Roboto', sans-serif;
    transform: translateX(-100%);
    opacity: 0;
    transition: all 0.3s ease;
    position: absolute;
    height: 100%;
    z-index: 10;
  }
  
  .history-panel.open {
    transform: translateX(0);
    opacity: 1;
    position: relative;
  }
  
  .chat-container.with-history {
    margin-left: 1rem;
    flex: 1;
  }
    .history-header {
    padding: 2rem 1.5rem 1rem 1.5rem;
    border-bottom: 1px solid #f0f0f0;
    font-weight: 500;
    color: #222;
    font-size: 1.1rem;
    font-family: 'Roboto', sans-serif;
  }
  
  .conversations-list {
    padding: 1rem;
    flex: 1;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #e0e0e0 transparent;
  }
  
  .conversations-list::-webkit-scrollbar {
    width: 6px;
  }
  
  .conversations-list::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .conversations-list::-webkit-scrollbar-thumb {
    background-color: #e0e0e0;
    border-radius: 3px;
  }
  
  .conversation-item {
    padding: 1rem 0.75rem;
    margin-bottom: 0.5rem;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    font-family: 'Roboto', sans-serif;
  }
  
  .conversation-item:hover {
    background: #f8f9fa;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
    .conversation-item.current {
    background: #e9ecef;
    border-color: #666;
    transform: none;
  }
  
  .conversation-title {
    font-weight: 500;
    margin-bottom: 0.4rem;
    font-size: 0.95rem;
    line-height: 1.3;
    color: #222;
    font-family: 'Roboto', sans-serif;
  }
  
  .conversation-date {
    font-size: 0.8rem;
    color: #666;
    font-family: 'Roboto', sans-serif;
  }
    .title-edit {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .title-edit input {
    flex: 1;
    font-size: 0.95rem;
    padding: 0.4rem 0.6rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-family: 'Roboto', sans-serif;
    outline: none;
    transition: border-color 0.2s ease;
  }
  
  .title-edit input:focus {
    border-color: #1976d2;
  }
  
  .title-edit-buttons {
    display: flex;
    gap: 0.25rem;
  }
  
  .title-edit-btn {
    background: none;
    border: none;
    padding: 0.3rem;
    cursor: pointer;
    border-radius: 4px;
    font-size: 0.85rem;
    min-width: auto;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  
  .title-edit-btn:hover {
    background: #f0f0f0;
    transform: scale(1.1);
  }
  
  .title-edit-btn.save {
    color: #1976d2;
  }
  
  .title-edit-btn.cancel {
    color: #666;
  }
  
  .conversation-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }
    .edit-title-btn {
    background: none;
    border: none;
    padding: 0.3rem;
    cursor: pointer;
    opacity: 0;
    transition: all 0.2s ease;
    font-size: 0.85rem;
    border-radius: 4px;
    min-width: auto;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
  }
  
  .conversation-item:hover .edit-title-btn {
    opacity: 1;
  }
  
  .edit-title-btn:hover {
    background: #f0f0f0;
    color: #333;
    transform: scale(1.1);
  }
  
  .no-conversations {
    text-align: center;
    color: #666;
    padding: 3rem 1rem;
    font-size: 0.9rem;
    font-family: 'Roboto', sans-serif;
    line-height: 1.5;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .chat-layout {
      max-width: 100%;
      padding: 0 1rem;
    }
    
    .history-panel {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100vh;
      z-index: 1000;
      margin-right: 0;
      border-radius: 0;
      transform: translateX(-100%);
    }
    
    .history-panel.open {
      transform: translateX(0);
    }
    
    .chat-container {
      max-width: 100%;
      border-radius: 12px;
      margin: 0;
    }
    
    .chat-container.with-history {
      margin-left: 0;
    }
    
    .history-header {
      padding-top: 3rem;
    }
  }

  @media (max-width: 480px) {
    .chat-header {
      padding: 0 1rem;
      font-size: 1.1rem;
    }
    
    .messages {
      padding: 0 1rem;
    }
    
    .chat-input {
      padding: 1rem;
    }
      .user-button {
      font-size: 0.8rem;
      padding: 0.4rem 0.8rem;
    }
  }

  /* Mobile backdrop */
  .backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }
  
  .backdrop.open {
    opacity: 1;
    visibility: visible;
  }
    @media (min-width: 769px) {
    .backdrop {
      display: none;
    }
  }

  .mobile-close {
    display: none;
  }

  @media (max-width: 768px) {
    .mobile-close {
      display: block !important;
    }
  }
</style>

<div class="chat-layout">  <!-- Mobile backdrop -->
  <div 
    class="backdrop" 
    class:open={showHistory} 
    role="button" 
    tabindex="0"
    on:click={() => showHistory = false}
    on:keydown={(e) => e.key === 'Escape' && (showHistory = false)}
    aria-label="Close conversation history"
  ></div>
  
  <!-- History Panel -->
  <div class="history-panel" class:open={showHistory}>
    <div class="history-header">
      Conversation History
      <!-- Mobile close button -->
      <button 
        class="mobile-close" 
        on:click={() => showHistory = false}
        style="display: none; position: absolute; top: 1.5rem; right: 1.5rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; padding: 0.5rem;"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
      </button>
    </div>
    <div class="conversations-list">
      {#each conversations as conversation}
        <div 
          class="conversation-item" 
          class:current={conversation.sessionId === sessionId}
          on:click={() => loadConversation(conversation.sessionId)}
        >          {#if editingTitleSessionId === conversation.sessionId}
            <div class="title-edit" on:click|stopPropagation>
              <input 
                type="text" 
                bind:value={editingTitle} 
                on:keydown={(e) => e.key === 'Enter' && saveTitle(conversation.sessionId)}
                on:keydown={(e) => e.key === 'Escape' && cancelEditingTitle()}
                on:click|stopPropagation
              />
              <div class="title-edit-buttons">
                <button class="title-edit-btn save" on:click|stopPropagation={() => saveTitle(conversation.sessionId)}>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                </button>
                <button class="title-edit-btn cancel" on:click|stopPropagation={cancelEditingTitle}>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                  </svg>
                </button>
              </div>
            </div>
          {:else}
            <div class="conversation-actions">
              <div>
                <div class="conversation-title">{conversation.title || 'Untitled Conversation'}</div>
                <div class="conversation-date">{new Date(conversation.lastActivity).toLocaleDateString()}</div>
              </div>              <button 
                class="edit-title-btn" 
                on:click|stopPropagation={() => startEditingTitle(conversation.sessionId, conversation.title)}
                title="Edit title"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14.06 9.02l.92.92L5.92 19H5v-.92l9.06-9.06M17.66 3c-.25 0-.51.1-.7.29l-1.83 1.83 3.75 3.75 1.83-1.83c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29zm-3.6 3.19L3 17.25V21h3.75L17.81 9.94l-3.75-3.75z"/>
                </svg>
              </button>
            </div>
          {/if}
        </div>
      {/each}      {#if conversations.length === 0}
        <div class="no-conversations">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="#bbb" style="margin-bottom: 1rem;">
            <path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4C22,2.89 21.1,2 20,2Z"/>
          </svg>
          <div>No conversations yet</div>
          <div style="font-size: 0.8rem; color: #999; margin-top: 0.5rem;">Start a new conversation to see it here</div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Main Chat Container -->
  <div class="chat-container" class:with-history={showHistory}>    <div class="chat-header">
      <div class="header-controls">
        <button 
          class="control-button" 
          on:click={startNewChat}
          title="New Chat"
        >
          <svg class="control-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>
          </svg>
        </button>        <button 
          class="control-button" 
          class:active={showHistory}
          on:click={toggleHistory}
          title="Toggle conversation history"
        >
          <svg class="control-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/>
          </svg>
        </button>
        <span>Scalable Chat</span>
      </div>      <div class="user-selector">
        <div class="user-dropdown">
          <button class="user-button" on:click={() => showUserDropdown = !showUserDropdown}>
            <span>{selectedUser.name}</span>
            <span>▼</span>
          </button>
          {#if showUserDropdown}
            <div class="user-menu">
              {#each USERS as user}
                <div 
                  class="user-menu-item" 
                  class:selected={user.userId === selectedUser.userId}
                  on:click={() => { switchUser(user); showUserDropdown = false; }}
                >
                  <div>{user.name}</div>
                  <div style="font-size: 0.75rem; color: #666;">{user.email}</div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
        <button 
          class="control-button"
          on:click={toggleMemory}
          title="View user memory"
        >
          <svg class="control-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
        </button>
      </div>
    </div>
    <div bind:this={messagesContainer} class="messages">
      {#each messages as message (message.id)}
        <div class="message" class:user={message.sender === 'user'} class:assistant={message.sender === 'assistant'} class:isLoading={message.isLoading} class:isError={message.isError}>
          <div class="content">{message.content}</div>
        </div>
      {/each}
    </div>
    <form on:submit|preventDefault={send} class="chat-input">
      <input type="text" bind:value={question} placeholder="Type your message..." />
      <button type="submit">Send</button>
    </form>  </div>
    <!-- Memory Panel -->
  {#if showMemory}
    <!-- Backdrop -->
    <div class="memory-backdrop" on:click={() => showMemory = false}></div>
    
    <div class="memory-panel">      <div class="memory-header">
        <h3>User Memory for {selectedUser.name}</h3>
        <div class="memory-header-actions">
          {#if userMemory}
            <button class="delete-memory-button" on:click={deleteUserMemory} title="Delete all memories">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
              </svg>
            </button>
          {/if}
          <button class="close-button" on:click={() => showMemory = false}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
      </div>
      <div class="memory-content">
        {#if userMemory}
          <div class="memory-section">
            <h4>Work Profile</h4>
            {#if userMemory.work_profile && userMemory.work_profile.length > 0}
              <ul>
                {#each userMemory.work_profile as item}
                  <li>{item}</li>
                {/each}
              </ul>
            {:else}
              <p class="no-data">No work profile information</p>
            {/if}
          </div>

          <div class="memory-section">
            <h4>Interests</h4>
            {#if userMemory.interests && userMemory.interests.length > 0}
              <ul>
                {#each userMemory.interests as interest}
                  <li>{interest}</li>
                {/each}
              </ul>
            {:else}
              <p class="no-data">No interests recorded</p>
            {/if}
          </div>

          <div class="memory-section">
            <h4>Knowledge Areas</h4>
            {#if userMemory.knowledge && userMemory.knowledge.length > 0}
              <ul>
                {#each userMemory.knowledge as knowledge}
                  <li>{knowledge}</li>
                {/each}
              </ul>
            {:else}
              <p class="no-data">No knowledge areas recorded</p>
            {/if}
          </div>

          <div class="memory-section">
            <h4>Goals</h4>
            {#if userMemory.goals && userMemory.goals.length > 0}
              <ul>
                {#each userMemory.goals as goal}
                  <li>{goal}</li>
                {/each}
              </ul>
            {:else}
              <p class="no-data">No goals recorded</p>
            {/if}
          </div>

          <div class="memory-section">
            <h4>Family & Friends</h4>
            {#if userMemory.family_and_friends && userMemory.family_and_friends.length > 0}
              <ul>
                {#each userMemory.family_and_friends as person}
                  <li>{person}</li>
                {/each}
              </ul>
            {:else}
              <p class="no-data">No family/friends information</p>
            {/if}
          </div>

          <div class="memory-section">
            <h4>Preferences</h4>
            {#if userMemory.personal_preferences && userMemory.personal_preferences.length > 0}
              <div class="subsection">
                <h5>Personal:</h5>
                <ul>
                  {#each userMemory.personal_preferences as pref}
                    <li>{pref}</li>
                  {/each}
                </ul>
              </div>
            {/if}
            {#if userMemory.output_preferences && userMemory.output_preferences.length > 0}
              <div class="subsection">
                <h5>Output:</h5>
                <ul>
                  {#each userMemory.output_preferences as pref}
                    <li>{pref}</li>
                  {/each}
                </ul>
              </div>
            {/if}
            {#if userMemory.assistant_preferences && userMemory.assistant_preferences.length > 0}
              <div class="subsection">
                <h5>Assistant:</h5>
                <ul>
                  {#each userMemory.assistant_preferences as pref}
                    <li>{pref}</li>
                  {/each}
                </ul>
              </div>
            {/if}
            {#if (!userMemory.personal_preferences || userMemory.personal_preferences.length === 0) && 
                 (!userMemory.output_preferences || userMemory.output_preferences.length === 0) && 
                 (!userMemory.assistant_preferences || userMemory.assistant_preferences.length === 0)}
              <p class="no-data">No preferences recorded</p>
            {/if}
          </div>

          <div class="memory-section">
            <h4>Dislikes</h4>
            {#if userMemory.dislikes && userMemory.dislikes.length > 0}
              <ul>
                {#each userMemory.dislikes as dislike}
                  <li>{dislike}</li>
                {/each}
              </ul>
            {:else}
              <p class="no-data">No dislikes recorded</p>
            {/if}
          </div>
        {:else}
          <div class="no-memory">
            <p>No memory data available</p>
            <p>Start chatting to build user memory</p>
          </div>
        {/if}
      </div>
    </div>
  {/if}
</div>
