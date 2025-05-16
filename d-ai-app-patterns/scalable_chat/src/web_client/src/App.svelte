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
  body, .page {
    background: #fafbfc;
    min-height: 100vh;
    margin: 0;
    padding: 0;
  }
  .page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2.5rem 0;
  }
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
  }
  .chat-header {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 500;
    color: #222;
    margin-bottom: 1.5rem;
    letter-spacing: 0.01em;
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
