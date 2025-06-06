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
  let messagesContainer;
  let selectedUser = USERS[0]; // Default to first user
  let showUserDropdown = false;
  const API_URL = import.meta.env.API_URL || window._env_?.API_URL;
  const SSE_URL = import.meta.env.SSE_URL || window._env_?.SSE_URL;
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
    } catch (error) {
      console.error('Failed to start session:', error);
      sessionId = crypto.randomUUID();
      localStorage.setItem('session_id', sessionId);
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
            const dataStr = line.substring(6);
            if (dataStr === '__END__') {
              messages = messages.map(msg => 
                msg.id === assistantMessagePlaceholder.id ? { ...msg, isLoading: false } : msg
              );
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
    }
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
  }  .chat-header {
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
  }
  .user-button:hover {
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
  }
  .user-menu-item.selected {
    background: #e3f2fd;
    color: #1976d2;
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
  }
  input:focus {
    border: 1.5px solid #b3cdf6;
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
</style>

<div class="chat-container">
  <div class="chat-header">
    <span>Scalable Chat</span>
    <div class="user-selector">
      <div class="user-dropdown">        <button class="user-button" on:click={() => showUserDropdown = !showUserDropdown}>
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
  </form>
</div>
