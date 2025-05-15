<script>
  import { onMount } from 'svelte';
  let question = '';
  let messages = [];
  let sessionId;
  // Determine base API URL: Vite dev or injected env.js
  const API_URL = import.meta.env.VITE_API_URL || window._env_?.API_URL;

  onMount(() => {
    sessionId = localStorage.getItem('session_id') || crypto.randomUUID();
    localStorage.setItem('session_id', sessionId);
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
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 600px;
    margin: 0 auto;
  }
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
  }
  .message {
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    border-radius: 4px;
  }
  .message.user {
    background-color: #daf1ff;
    align-self: flex-end;
  }
  .message.assistant {
    background-color: #f1f0f0;
    align-self: flex-start;
  }
  form {
    display: flex;
    padding: 1rem;
    border-top: 1px solid #ddd;
  }
  input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    margin-left: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: #008cff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>

<div class="chat-container">
  <div class="messages">
    {#each messages as msg}
      <div class="message {msg.sender}">{msg.content}</div>
    {/each}
  </div>
  <form on:submit|preventDefault={send}>
    <input bind:value={question} placeholder="Type your message..." autocomplete="off" />
    <button type="submit">Send</button>
  </form>
</div>
