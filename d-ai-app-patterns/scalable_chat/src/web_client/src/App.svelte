<script>
  import { onMount, afterUpdate } from 'svelte';
  let question = '';
  let messages = [];
  let sessionId;
  let messagesContainer;
  const API_URL = import.meta.env.VITE_API_URL || window._env_?.API_URL;

  onMount(() => {
    sessionId = localStorage.getItem('session_id') || crypto.randomUUID();
    localStorage.setItem('session_id', sessionId);
  });

  afterUpdate(() => {
    // Auto-scroll to bottom on new messages
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  });

  async function send() {
    if (!question.trim()) return;
    console.log('Sending question to API URL:', API_URL);
    // Append user message
    messages = [...messages, { sender: 'user', content: question }];
    // Prepare placeholder for assistant response
    messages = [...messages, { sender: 'assistant', content: '' }];
    const assistantIndex = messages.length - 1;
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, question }),
      });
      if (!res.ok) {
        console.error('Fetch error:', res.status, res.statusText);
        return;
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      // Stream and parse SSE-like chunks
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const parts = chunk.split('\n\n');
        for (const part of parts) {
          if (part.startsWith('data: ')) {
            const data = part.slice(6).trim();
            if (data === '__END__') {
              // End of message
              break;
            } else {
              // Update streamed content
              messages[assistantIndex].content += data;
              messages = [...messages];
            }
          }
        }
      }
    } catch (err) {
      console.error('Error in send():', err);
    } finally {
      question = '';
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 600px;
    margin: 0 auto;
    background-color: #e5ddd5;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
  }
  .chat-header {
    padding: 1rem;
    background-color: #008cff;
    color: white;
    text-align: center;
    font-size: 1.5rem;
    flex-shrink: 0;
  }
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
  }
  .message {
    display: flex;
    align-items: flex-end;
    max-width: 70%;
    padding: 0.75rem;
    margin: 0.5rem 0;
    word-wrap: break-word;
    font-size: 1.1rem;
  }
  .message.user {
    background-color: #dcf8c6;
    align-self: flex-end;
    margin-left: auto;
    margin-right: 0.5rem;
    flex-direction: row-reverse;
    border-radius: 16px 16px 16px 0;
  }
  .message.assistant {
    background-color: #ffffff;
    align-self: flex-start;
    margin-right: auto;
    margin-left: 0.5rem;
    flex-direction: row;
    border-radius: 16px 16px 0 16px;
  }
  .icon {
    font-size: 1.2rem;
    margin: 0 0.5rem;
  }
  .content {
    flex: 1;
  }
  .chat-input {
    position: sticky;
    bottom: 0;
    background: white;
    padding: 0.5rem 1rem;
    border-top: 1px solid #ccc;
    display: flex;
    flex-shrink: 0;
  }
  input {
    flex: 1;
    padding: 0.75rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    margin-left: 0.5rem;
    padding: 0.75rem 1.5rem;
    background-color: #008cff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }
</style>

<div class="chat-container">
  <div class="chat-header">Scalable Chat</div>
  <div bind:this={messagesContainer} class="messages">
    {#each messages as msg}
      <div class="message {msg.sender}">
        <span class="icon">{msg.sender === 'user' ? '👤' : '🤖'}</span>
        <div class="content">{msg.content}</div>
      </div>
    {/each}
  </div>
  <form on:submit|preventDefault={send} class="chat-input">
    <input bind:value={question} placeholder="Type your message..." autocomplete="off" />
    <button type="submit">Send</button>
  </form>
</div>
